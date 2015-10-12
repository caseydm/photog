# project/views.py

import uuid, random
from flask import Flask, redirect, render_template, \
    request, url_for, flash, current_app
from flask.ext.stormpath import StormpathManager, login_required, \
    groups_required, user, User
from stormpath.error import Error as StormpathError
from flask.ext.login import login_user
from flask.ext.sqlalchemy import SQLAlchemy
from forms import RegistrationForm, AddContactForm, AddUserForm


# app setup
app = Flask(__name__, instance_relative_config=True)

# app conig
app.config.from_object('config')
app.config.from_pyfile('config.py')

# stormpath setup
stormpath_manager = StormpathManager(app)

# database setup
db = SQLAlchemy(app)

from models import Contact


################
# static pages #
################

# index
@app.route('/')
def index():
    return render_template('index.html')


#############
# dashboard #
#############

# dashboard home
@app.route('/dashboard/')
@login_required
def dashboard():
    contacts = db.session.query(Contact).filter_by(
        tenant_id=user.custom_data['tenant_id']).order_by(Contact.name.asc())
    return render_template('dashboard/dashboard.html', user=user, contacts=contacts)


# profile
@app.route('/account/')
@login_required
def account():
    return render_template('dashboard/account.html', user=user)


# new contact
@app.route('/new_contact/', methods=['GET', 'POST'])
@login_required
def new_contact():
    """
    Add new contact
    """
    form = AddContactForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_contact = Contact(
                form.name.data,
                form.email.data,
                user.username,
                user.custom_data['tenant_id']
            )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('new_contact.html', form=form)


###################
# accounts #
###################

# random password function
def create_password():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    upperalphabet = alphabet.upper()
    pw_len = 20
    pwlist = []

    for i in range(pw_len//3):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
        pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
        pwlist.append(str(random.randrange(10)))
    for i in range(pw_len-len(pwlist)):
        pwlist.append(alphabet[random.randrange(len(alphabet))])

    random.shuffle(pwlist)
    pwstring = "".join(pwlist)

    return(pwstring)


# register
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
                data['custom_data'] = {
                    'tenant_id': tenant_id,
                    'site_admin': 'True'
                }

                # Create the user account on Stormpath.  If this fails, an
                # exception will be raised.
                account = User.create(**data)

                # create a new stormpath group
                directory = stormpath_manager.application.default_account_store_mapping.account_store
                tenant_group = directory.groups.create({
                    'name': tenant_id,
                    'description': data['email']
                })

                # assign new user to the newly created group
                account.add_group(tenant_group)
                account.add_group('site_admin')

                # If we're able to successfully create the user's account,
                # we'll log the user in (creating a secure session using
                # Flask-Login), then redirect the user to the
                # STORMPATH_REDIRECT_URL setting.
                login_user(account, remember=True)

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
        'account/register.html',
        form=form,
    )


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@groups_required(['site_admin'])
def add_user():
    """
    Add a user to an account
    """
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            data = form.data

            # set tenant id to same as current logged in user
            tenant_id = user.custom_data['tenant_id']

            # given_name and surname are required fields
            data['given_name'] = 'Anonymous'
            data['surname'] = 'Anonymous'

            # set tenant id and site_admin status
            data['custom_data'] = {
                'tenant_id': tenant_id,
                'site_admin': 'False'
            }

            # generate random password
            data['password'] = create_password()

            # create account
            account = User.create(**data)

            # add user to tenant group
            account.add_group(tenant_id)

            # send password reset email
            current_app.stormpath_manager.application.send_password_reset_email('caseym@gmail.com')

            # flash or redirect
            flash('Account created')
        except StormpathError as err:
                flash(err.message.get('message'))
    return render_template('dashboard/add_user.html', form=form)
