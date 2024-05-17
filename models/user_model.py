from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy ORM instance
db = SQLAlchemy()


class User(db.Model):
    """
    User model that represents user details in the database.
    """
    __tablename__ = 'users'

    uuid = db.Column(db.String(36), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(db.Model):
    """
    Transaction model to store transactions related to users.
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(36), db.ForeignKey('users.uuid'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db(app):
    """
    Initializes the database within an application context, creating all tables.
    This function should be called from the Flask application factory.
    """
    with app.app_context():
        db.init_app(app)
        db.create_all()
