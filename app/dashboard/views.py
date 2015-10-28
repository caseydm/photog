from flask import render_template, redirect, url_for
from flask.ext.stormpath import login_required, user
from . import dashboard
from .forms import AddContactForm
from .models import Contact
from app import db


# dashboard home
@dashboard.route('/dashboard/')
@login_required
def dashboard_home():
    contacts = db.session.query(Contact).filter_by(
         tenant_id=user.custom_data['tenant_id']).order_by(Contact.name.asc())
    return render_template('dashboard/dashboard.html', user=user, contacts=contacts)


# profile
@dashboard.route('/account/')
@login_required
def account():
    # get group accounts
    group = user.groups.search({'name': user.custom_data['tenant_id']})
    group = group[0]
    accounts = group.accounts
    return render_template(
        'dashboard/account.html',
        user=user,
        accounts=accounts
    )


# new contact
@dashboard.route('/newcontact/', methods=['GET', 'POST'])
@login_required
def new_contact():
    form = AddContactForm()

    if form.validate_on_submit():
        new_contact = Contact(
            form.name.data,
            form.email.data,
            form.phone.data,
            user.get_id(),
            user.custom_data['tenant_id']
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template('dashboard/add_contact.html', form=form)