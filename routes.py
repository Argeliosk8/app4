from app import app
from forms import *
from flask import Flask, render_template, redirect, url_for, request
from models import *
from flask_login import login_required, login_user, LoginManager, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return "Sorry your must be logged in to view this page"

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user', username = current_user.username))
        else:
            return redirect(url_for('error'))
    return render_template('login.html', form = form)


@app.route('/profile/<username>', methods = ['POST', 'GET'])
@login_required
def user(username):
  if username == current_user.username:
    my_vehicles = Vehicle.query.filter_by(user_id = current_user.id)
    form = AddVehicleForm(csrf_enabled=False)  
    if form.validate_on_submit():
      new_vehicle = Vehicle(brand = form.brand.data, model = form.model.data, user_id = current_user.id)
      db.session.add(new_vehicle)
      db.session.commit()
      return redirect(url_for('user', username = username))
    if my_vehicles is None:
      my_vehicles = []
      return render_template('user.html', user=user, my_vehicles = my_vehicles, form = form)
    else:      
        return render_template('user.html', user=user, my_vehicles = my_vehicles, form = form)

  
@app.route('/profile/<username>/delete/<int:vehicle_id>')
@login_required
def delete_vehicle(username, vehicle_id):
    if username == current_user.username:
        vehicle_to_delete = Vehicle.query.get(vehicle_id)    
        if vehicle_to_delete:
            db.session.delete(vehicle_to_delete)
            db.session.commit()
            return redirect(url_for('user', username = username))
        else: 
            return redirect(url_for('user', username = username))
      


@app.route('/error')
def error():    
    return render_template('error.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
