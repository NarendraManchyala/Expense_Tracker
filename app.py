import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Transaction, Trip
from datetime import datetime

app = Flask(__name__)

# Local DB URI - Replace this with DATABASE_URL in production (like Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://postgres:1224@localhost:5432/expense_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/add', methods=["GET", "POST"])
def add_transaction():
    trips = Trip.query.all()  # For dropdown
    if request.method == "POST":
        amount = float(request.form['amount'])
        category = request.form['category']
        type_ = request.form['type']
        description = request.form['description']
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        trip_id = request.form.get('trip_id')
        trip_id = int(trip_id) if trip_id else None

        new_transaction = Transaction(
            amount=amount,
            category=category,
            type=type_,
            description=description,
            date=date_obj,
            trip_id=trip_id
        )

        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("add_transaction"))
    return render_template('addExpenses.html', trips=trips)

@app.route('/trip', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        trip_name = request.form['trip_name']
        destination = request.form['destination']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        budget = float(request.form['budget'])
        description = request.form['description']

        new_trip = Trip(
            trip_name=trip_name,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            description=description
        )
        db.session.add(new_trip)
        db.session.commit()
        return redirect(url_for("add_trip"))
    return render_template("trips.html")

@app.route('/viewTrip')
def view_trips():
    trips = Trip.query.all()
    return render_template('viewTrips.html', trips=trips)

@app.route('/editTrip/<int:trip_id>', methods=['GET', 'POST'])
def edit_details(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if request.method == 'POST':
        trip.trip_name = request.form['trip_name']
        trip.destination = request.form['destination']
        trip.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        trip.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        trip.budget = float(request.form['budget'])
        trip.description = request.form['description']

        db.session.commit()
        return redirect(url_for('view_trips'))
    return render_template('edit_trips.html', trip=trip)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    #app.run(debug=True)