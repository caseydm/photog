from flask import render_template
from flask.ext.stormpath import login_required, user
from . import dashboard


# dashboard home
@dashboard.route('/dashboard/')
@login_required
def dashboard():
    # contacts = db.session.query(Contact).filter_by(
    #     tenant_id=user.custom_data['tenant_id']).order_by(Contact.name.asc())
    return render_template('dashboard/dashboard.html', user=user)


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
# @mod.route('/new_contact/', methods=['GET', 'POST'])
# @login_required
# def new_contact():
#     """
#     Add new contact
#     """
#     form = AddContactForm(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             new_contact = Contact(
#                 form.name.data,
#                 form.email.data,
#                 user.username,
#                 user.custom_data['tenant_id']
#             )
#         db.session.add(new_contact)
#         db.session.commit()
#         return redirect(url_for('dashboard'))
#     return render_template('new_contact.html', form=form)