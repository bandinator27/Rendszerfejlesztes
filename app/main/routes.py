from flask import Flask, redirect, url_for, render_template, request, session, flash

from app.database import db
from app.blueprints import main_bp
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *

#@main_bp.route("/")
#def home():
#    if "user" in session:
#        user = session["user"]
#    else:
#        user = "No session"
#    return render_template('index.html', user=user)

#@main_bp.route("/login/", methods=['GET', 'POST'])
#def login():
#        return render_template('login.html', register = url_for('main.register'))

#regisztráció
#@main_bp.route("/register/", methods=['GET', 'POST'])
#def register():
#        return render_template('register.html')

# userek kilistázása adatbázis teszteléshez
#@main_bp.route("/view/")
#def view():
#    return render_template('view.html', values=db.session.query(Users).all())

# autók kilistázása adatbázis teszteléshez
#@main_bp.route("/cars/")
#def cars():
#    return render_template('cars.html', values=db.session.query(Cars).all())

# session nullázás
#@main_bp.route("/logout/")
#def logout():
#    if "user" in session:
#        session.pop("user", None)
#        session.pop("role", None)
#        flash("You have been logged out!", "info")
#    return redirect(url_for("main.login"))

#@main_bp.route("/admin/")
#def admin_page():
#    if "role" in session:
#        role = session["role"]
#        if role == "Admin":
#            return render_template('admin.html')
#        else:
#            return redirect(url_for("main.home"))
#    else:
#        return redirect(url_for("main.home"))
    
#@main_bp.route("/account/")
#def account():
#    if "user" in session:
#        user = session["user"]
#        found_user = db.session.query(Users).filter_by(username=user).first()
#        if found_user:
#            return render_template('account.html', userAccount=found_user)
#        else:
#            return redirect(url_for("main.home"))
#    else:
#        return redirect(url_for("main.home"))