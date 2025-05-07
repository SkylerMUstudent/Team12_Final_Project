from flask import render_template, session, redirect, url_for, request
from . import admin_bp
from models import db, Reservation

@admin_bp.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))

    reservations = Reservation.query.all()
    total_sales = sum(r.price for r in reservations)

    # Build seating chart (12 rows, 4 seats per row)
    seats = [['Available' for _ in range(4)] for _ in range(12)]
    for res in reservations:
        seats[res.seat_row - 1][res.seat_col - 1] = f"{res.first_name[0]}.{res.last_name[0]}"

    return render_template('admin_dashboard.html', reservations=reservations, total_sales=total_sales, seats=seats)


@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    res = Reservation.query.get(id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))