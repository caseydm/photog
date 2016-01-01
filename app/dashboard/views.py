from flask import render_template, redirect, url_for, request, flash
from flask.ext.stormpath import login_required, groups_required, user
from . import dashboard
from .forms import AddContactForm, AddNoteForm
from .models import Contact, Note
from app import db
from app import stormpath_manager


# dashboard home
@dashboard.route('/dashboard/')
@login_required
def dashboard_home():
    contacts = db.session.query(Contact).filter_by(
         tenant_id=user.custom_data['tenant_id']).order_by(Contact.created_date.desc())
    return render_template('dashboard/dashboard.html', user=user, contacts=contacts)


# profile
@dashboard.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    # get group accounts
    group = user.groups.search({'name': user.custom_data['tenant_id']})
    group = group[0]
    accounts = group.accounts
    if request.method == 'POST':
        user.given_name = request.form['name']
        user.save()
    return render_template(
        'dashboard/account.html',
        user=user,
        accounts=accounts
    )

### Contacts ###

# create contact
@dashboard.route('/newcontact/', methods=['GET', 'POST'])
@login_required
def new_contact():
    form = AddContactForm()

    if form.validate_on_submit():
        new_contact = Contact(
            form.name.data,
            form.email.data,
            form.phone.data,
            form.comment.data,
            form.lead_source.data,
            user.get_id(),
            user.custom_data['tenant_id']
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template('dashboard/add_contact.html', action='Add', form=form)


# read contact (detail)
@dashboard.route('/contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def contact_detail(contact_id):
    form = AddNoteForm()

    contact = Contact.query.filter_by(
        id=contact_id, tenant_id=user.custom_data['tenant_id']).first_or_404()
    notes = contact.notes

    if form.validate_on_submit():
        new_note = Note(
            form.content.data,
            user.get_id(),
            user.custom_data['tenant_id'],
            contact.id
        )
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('dashboard.contact_detail', contact_id=contact.id))

    return render_template(
        'dashboard/contact_detail.html',
        contact=contact,
        notes=notes,
        form=form
        )


# update contact
@dashboard.route('/editcontact/<contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    form = AddContactForm()

    contact = Contact.query.filter_by(
        id=contact_id, tenant_id=user.custom_data['tenant_id']).first_or_404()

    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone = form.phone.data
        contact.lead_source = form.lead_source.data
        contact.comment = form.comment.data

        db.session.commit()
        return redirect(url_for('dashboard.contact_detail', contact_id=contact.id))

    form.name.data = contact.name
    form.email.data = contact.email
    form.phone.data = contact.phone
    form.lead_source.data = contact.lead_source
    form.comment.data = contact.comment

    return render_template('dashboard/add_contact.html', action='Edit', form=form)


# delete contact
@dashboard.route('/contact/delete/<contact_id>', methods=['GET'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.filter_by(
        id=contact_id, tenant_id=user.custom_data['tenant_id']).first_or_404()

    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted')
    return redirect(url_for('dashboard.dashboard_home'))


@dashboard.context_processor
def utility_processor():
    def get_user(user_id):
        return stormpath_manager.client.accounts.get(user_id)
    return dict(get_user=get_user)
