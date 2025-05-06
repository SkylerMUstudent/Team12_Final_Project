import random, string
from flask import render_template, request, redirect, url_for
from . import reservation_bp
from models import db, Reservation

COST_MATRIX = [[54, 57, 74, 77], [77, 19, 93, 31], [46, 97, 80, 98],
               [98, 22, 68, 75], [49, 97, 56, 98], [93, 13, 86, 88],
               [12, 58, 65, 39], [87, 46, 88, 81], [37, 25, 77, 72],
               [9, 20, 80, 69], [79, 47, 64, 82], [99, 88, 49, 29]]

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@reservation_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        row = int(request.form['seat_row']) - 1
        col = int(request.form['seat_col']) - 1
        price = COST_MATRIX[row][col]
        code = generate_code()
        reservation = Reservation(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            seat_row=row + 1,
            seat_col=col + 1,
            price=price,
            code=code
        )
        db.session.add(reservation)
        db.session.commit()
        return render_template('confirmation.html', code=code, price=price)
    return render_template('reserve.html')