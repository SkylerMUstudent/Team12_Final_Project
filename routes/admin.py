from flask import render_template, session, redirect, url_for, request
from . import admin_bp
from models import db, Reservation, Admin

# Admin login route
@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Authenticate admin
        admin_user = Admin.query.filter_by(username=username, password=password).first()

        if admin_user:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_dashboard')) 
        else:
            error = "Invalid credentials. Please try again."

    return render_template('admin_login_dashboard.html', logged_in=False, error=error)


# Admin dashboard route
@admin_bp.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login')) 

    reservations = Reservation.query.all()
    total_sales = sum(r.price for r in reservations)
    seats = [['Available' for _ in range(4)] for _ in range(12)]
    
    for res in reservations:
        seats[res.seat_row - 1][res.seat_col - 1] = f"{res.first_name[0]}.{res.last_name[0]}"

    return render_template(
        'admin_login_dashboard.html',
        logged_in=True,
        reservations=reservations,
        total_sales=total_sales,
        seats=seats,
        error=None
    )


# Admin logout
@admin_bp.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.admin_login'))


# Delete a reservation
@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    res = Reservation.query.get(id)
    if res:
        db.session.delete(res)
        db.session.commit()
    
    return redirect(url_for('admin.admin_dashboard'))  
