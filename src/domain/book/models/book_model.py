from datetime import datetime
from sqlalchemy import DateTime, event
from uuid import uuid4
from config import db
from flask_jwt_extended import get_jwt_identity
from enum import Enum as PyEnum
from sqlalchemy import Enum


def get_uuid():
    return uuid4().hex

class Currency(PyEnum):
    KR = 'KR'
    USD = 'USD'
    EURO = 'EURO'

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(32), unique=True)
    price = db.Column(db.Float)
    currency = db.Column(
        Enum(Currency, create_constraint=True, native_enum=False),
        default=Currency.KR,
        nullable=False,
    )
    user_id = db.Column(
        db.ForeignKey('users.id'),
        default=lambda: get_jwt_identity()['id'], # The lambda function retrieve the user id from JWT
        nullable=False,
    )
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def json(self):
        # Define the JSON-serializable representation of the book
        currency_str = self.currency.value if self.currency else None
        return {
            "id": self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'price': self.price,
            'currency': currency_str,
            'user_id': self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Set up an event listener to automatically update the 'updated_at' field
@event.listens_for(Book, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()

