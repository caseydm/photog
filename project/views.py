# project/views.py

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request, session,
    url_for
)
from flask.ext.stormpath import (
    StormpathManager,
    login_required,
    user,
    User
)
from forms import RegistrationForm
from stormpath.error import Error as StormpathError
from flask.ext.login import login_user
import uuid


# config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
stormpath_manager = StormpathManager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user with Stormpath.
    """
    form = RegistrationForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():
        fail = False

        # Iterate through all fields, grabbing the necessary form data and
        # flashing error messages if required.
        data = form.data
        for field in data.keys():
            if app.config['STORMPATH_ENABLE_%s' % field.upper()]:
                if app.config['STORMPATH_REQUIRE_%s' % field.upper()] and not data[field]:
                    fail = True

                    # Manually override the terms for first / last name to make
                    # errors more user friendly.
                    if field == 'given_name':
                        field = 'first name'

                    elif field == 'surname':
                        field = 'last name'

                    flash('%s is required.' % field.replace('_', ' ').title())

        # If there are no missing fields (per our settings), continue.
        if not fail:

            # Attempt to create the user's account on Stormpath.
            try:

                # Since Stormpath requires both the given_name and surname
                # fields be set, we'll just set the both to 'Anonymous' if
                # the user has # explicitly said they don't want to collect
                # those fields.
                data['given_name'] = data['given_name'] or 'Anonymous'
                data['surname'] = data['surname'] or 'Anonymous'

                # create a tenant ID
                tenant_id = str(uuid.uuid4())
                data['custom_data'] = {"tenant_id": tenant_id}

                # Create the user account on Stormpath.  If this fails, an
                # exception will be raised.
                account = User.create(**data)

                # create a new stormpath group
                directory = stormpath_manager.application.default_account_store_mapping.account_store
                tenant_group = directory.groups.create({'name': tenant_id})

                # assign new user to the newly created group
                account.add_group(tenant_group)

                # If we're able to successfully create the user's account,
                # we'll log the user in (creating a secure session using
                # Flask-Login), then redirect the user to the
                # STORMPATH_REDIRECT_URL setting.
                login_user(account, remember=True)
                # user.custom_data['tenant_id'] = tenant_id
                # user.save()

                if 'STORMPATH_REGISTRATION_REDIRECT_URL'\
                        in app.config:
                    redirect_url = app.config[
                        'STORMPATH_REGISTRATION_REDIRECT_URL']
                else:
                    redirect_url = app.config['STORMPATH_REDIRECT_URL']
                return redirect(redirect_url)

            except StormpathError as err:
                flash(err.message.get('message'))

    return render_template(
        'register.html',
        form=form,
    )
