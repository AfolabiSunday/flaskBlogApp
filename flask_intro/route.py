##############################################################
#   intergrity error needs to be handle in the databes when useer try to update or register with an existing email
##################################################################

import os
import secrets
from PIL import Image
from flask import redirect, render_template, flash, url_for, request
from flask_intro.models import User, Post
from flask_intro.forms import RegistratForm, LoginForm, UpdateForm
from flask_intro import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/index')
def home():
    return render_template('home.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash(f'Login succesfully, welcome!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login not succesfully, Nice try!', 'danger')
    return render_template('login.html', title='Login Page', form=form)

@app.route('/register', methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistratForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data, email=form.Email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created Please Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='registrationForm', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
     

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.Email.data
        db.session.commit()
        flash('Details Successfully Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.Email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)