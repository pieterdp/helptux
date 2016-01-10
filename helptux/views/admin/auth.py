from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from helptux.modules.user.authentication import LoginForm
from helptux.modules.api.user import UserApi
from helptux.modules.error import DatabaseItemDoesNotExist
from helptux import app


@app.route('/admin/login', methods=['GET', 'POST'])
def v_login():
    form = LoginForm()
    a_user = UserApi()
    if form.validate_on_submit():
        try:
            user = a_user.get_by_user(form.email.data)
            print(user)
        except DatabaseItemDoesNotExist:
            # User does not exist
            flash('Invalid username or password.')
        else:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('helptux.v_index'))
            else:
                flash('Invalid username or password.')
    return render_template('admin/login.html', form=form)


@login_required
@app.route('/admin/logout', methods=['GET'])
def v_logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('helptux.v_index'))
