from datetime import datetime
from sqlalchemy import DateTime, event
from uuid import uuid4
from config import db

def get_uuid():
    return uuid4().hex

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    isbn = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def json(self):
        # Define the JSON-serializable representation of the book
        return {
            "id": self.id,
            'isbn': self.isbn,
            'author': self.author,
            'title': self.title,
            'price': self.price,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Set up an event listener to automatically update the 'updated_at' field
@event.listens_for(Book, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


