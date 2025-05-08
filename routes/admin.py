from flask import render_template, session, redirect, url_for, request, flash
from . import admin_bp
from models import db, Reservation
from models import Admin
import logging

@admin_bp.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #if username == 'admin' and password == 'pass':
        # Check if a matching admin exists in the database
        admin_user = Admin.query.filter_by(username=username, password=password).first()

        admins = Admin.query.all()
        for admin in admins:
            logging.warning(f"Username: {admin.username}, Password: {admin.password}")
        
        if admin_user:
            session['admin_logged_in'] = True
        else:
            session['admin_logged_in'] = False  # ✅ reset on failed login
            error = "Invalid credentials. Please try again."

    logged_in = session.get('admin_logged_in', False)

    reservations = []
    total_sales = 0
    seats = []

    if logged_in:
        reservations = Reservation.query.all()
        total_sales = sum(r.price for r in reservations)
        seats = [['Available' for _ in range(4)] for _ in range(12)]
        for res in reservations:
            seats[res.seat_row - 1][res.seat_col - 1] = f"{res.first_name[0]}.{res.last_name[0]}"

    return render_template(
        'admin_login_dashboard.html',
        logged_in=logged_in,
        reservations=reservations,
        total_sales=total_sales,
        seats=seats,
        error=error
    )


@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_dashboard'))

    res = Reservation.query.get(id)
    if res:
        db.session.delete(res)
        db.session.commit()
    
    return redirect(url_for('admin.admin_dashboard'))
