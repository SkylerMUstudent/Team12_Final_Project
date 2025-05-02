from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Reservation, Admin
from utils import get_cost_matrix
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/reservations.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin") # Default admin username
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "pass123") # Default admin password

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # Optional: seed one admin if none exist
    if not Admin.query.first():
        db.session.add(Admin(username="admin", password="password"))
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reserve", methods=["GET", "POST"])
def reserve():
    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        row = int(request.form["seat_row"])
        col = int(request.form["seat_column"])
        cost_matrix = get_cost_matrix()
        price = cost_matrix[row][col]
        reservation_code = f"{first[:2].upper()}{last[:2].upper()}{row}{col}"

        reservation = Reservation(
            first_name=first,
            last_name=last,
            seat_row=row,
            seat_column=col,
            reservation_code=reservation_code,
            price=price
        )
        db.session.add(reservation)
        db.session.commit()
        return f"Reservation successful! Code: {reservation_code}"
    return render_template("reserve.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials"

    return render_template('admin_login.html', error=error)

@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    reservations = Reservation.query.all()
    sales = sum(r.price for r in reservations)
    return render_template("admin_dashboard.html", reservations=reservations, sales=sales)

@app.route("/delete/<int:res_id>")
def delete(res_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    res = Reservation.query.get_or_404(res_id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))
