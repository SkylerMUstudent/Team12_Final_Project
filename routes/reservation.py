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

def build_seating_chart():
    chart = [["Available" for _ in range(4)] for _ in range(12)]
    reservations = Reservation.query.all()
    for r in reservations:
        chart[r.seat_row - 1][r.seat_col - 1] = f"{r.first_name[0]}.{r.last_name[0]}"
    return chart


@reservation_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    error = None

    if request.method == 'POST':
        try:
            row = int(request.form['seat_row'])
            col = int(request.form['seat_col'])

            # Validate bounds
            if row < 1 or row > 12 or col < 1 or col > 4:
                raise ValueError("Seat row must be 1–12 and column must be 1–4.")

            # Check if already reserved
            existing = Reservation.query.filter_by(seat_row=row, seat_col=col).first()
            if existing:
                raise ValueError(f"Seat Row {row}, Col {col} is already reserved.")

            price = COST_MATRIX[row - 1][col - 1]
            code = generate_code()

            reservation = Reservation(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                seat_row=row,
                seat_col=col,
                price=price,
                code=code
            )

            db.session.add(reservation)
            db.session.commit()

            # Build seating chart
            seats = build_seating_chart()

            return render_template('confirmation.html', code=code, price=price, seats=seats)

        except (ValueError, KeyError) as e:
            error = str(e)

    return render_template('reserve.html', error=error)

