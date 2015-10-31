# app/accounts/views.py

import uuid
import sendgrid
from manage import app
from app import stormpath_manager
from flask import redirect, render_template, \
    request, url_for, flash, abort
from flask.ext.stormpath import login_required, \
    groups_required, user, User
from stormpath.error import Error as StormpathError
from flask.ext.login import login_user
from .forms import RegistrationForm, AddUserForm
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridClientError, SendGridServerError
from . import accounts


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user with Stormpath.
    """
    form = RegistrationForm()

    # If we received a POST request with valid information, we'll continue
    # processing.
    if form.validate_on_submit():

        data = {}
        # Attempt to create the user's account on Stormpath.
        try:
            # email and password
            data['email'] = form.email.data
            data['password'] = form.password.data

            # given_name and surname are required fields
            data['given_name'] = 'Anonymous'
            data['surname'] = 'Anonymous'

            # create a tenant ID
            tenant_id = str(uuid.uuid4())
            data['custom_data'] = {
                'tenant_id': tenant_id,
                'site_admin': True
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

            # redirect to dashboard
            redirect_url = app.config['STORMPATH_REDIRECT_URL']
            return redirect(redirect_url)

        except StormpathError as err:
            flash(err.message.get('message'))

    return render_template(
        'account/register.html',
        form=form,
    )


@accounts.route('/add_user', methods=['GET', 'POST'])
@login_required
@groups_required(['site_admin'])
def add_user():
    """
    Send invite email with token to invited user
    """
    form = AddUserForm()

    if form.validate_on_submit():

        # token serializer
        ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        email = request.form['email']
        tenant_id = user.custom_data['tenant_id']

        # create token containing email and tenant_id
        token = ts.dumps([email, tenant_id])

        # create url with token, e.g. /add_user_confirm/asdf-asd-fasdf
        confirm_url = url_for(
            '.add_user_confirm',
            token=token,
            _external=True)

        try:
            # sendgrid setup
            sg = sendgrid.SendGridClient(
                app.config['SENDGRID_API_KEY'],
                raise_errors=True
            )

            # email setup
            message = sendgrid.Mail(
                to=request.form['email'],
                subject='Account Invitation',
                html='You have been invited to set up an account on PhotogApp. Click here: ' + confirm_url,
                from_email='support@photogapp.com'
            )

            # send email
            sg.send(message)

            flash('Invite sent successfully.')
            return render_template('dashboard/add_user_complete.html')

        # catch and display SendGrid errors
        except SendGridClientError as err:
            flash(err.message.get('message'))
        except SendGridServerError as err:
            flash(err.message.get('message'))
    return render_template('dashboard/add_user.html', form=form)


@accounts.route('/add_user_confirm/<token>', methods=['GET', 'POST'])
def add_user_confirm(token):
    """
    Decode invite token and create new user account
    """
    form = RegistrationForm()
    decoded = None
    try:
        ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        decoded = ts.loads(token, max_age=86400)
        email = decoded[0]
    except:
        abort(404)

    if form.validate_on_submit():
        try:
            tenant_id = decoded[1]

            data = {}
            data['email'] = email
            data['password'] = request.form['password']

            # given_name and surname are required fields
            data['given_name'] = 'Anonymous'
            data['surname'] = 'Anonymous'

            # set tenant id and site_admin status
            data['custom_data'] = {
                'tenant_id': tenant_id,
                'site_admin': 'False'
            }

            # create account
            account = User.create(**data)

            # add user to tenant group
            account.add_group(tenant_id)

            # login user
            login_user(account, remember=True)

            # success redirect
            return render_template('account/add_user_complete.html')
        except StormpathError as err:
            flash(err.message.get('message'))

    return render_template('account/add_user_setpassword.html',
                           form=form,
                           email=email)
