from flask import render_template, session, redirect, url_for, request
from . import admin_bp
from models import db, Reservation

@admin_bp.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    reservations = Reservation.query.all()
    total_sales = sum(r.price for r in reservations)
    return render_template('admin_dashboard.html', reservations=reservations, total_sales=total_sales)

@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    res = Reservation.query.get(id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))