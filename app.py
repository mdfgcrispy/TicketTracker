 HEAD
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ticket Model to store ticket data
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    profit_loss = db.Column(db.Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
    if request.method == 'POST':
        event_name = request.form['event_name']
        purchase_price = float(request.form['purchase_price'])
        selling_price = float(request.form['selling_price'])
        profit_loss = selling_price - purchase_price

        new_ticket = Ticket(
            event_name=event_name,
            purchase_price=purchase_price,
            selling_price=selling_price,
            profit_loss=profit_loss
        )

        db.session.add(new_ticket)
        db.session.commit()

        return redirect('/')

    return render_template('add_ticket.html')
