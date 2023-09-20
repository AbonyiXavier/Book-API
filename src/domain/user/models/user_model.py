from datetime import datetime
from sqlalchemy import DateTime, event
from uuid import uuid4
from extensions import db

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    first_name = db.Column(db.String(345), nullable=False)
    last_name = db.Column(db.String(345), nullable=False)
    email = db.Column(db.String(345), unique=True)
    jti = db.Column(db.String(36), index=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def json(self):
        # Define the JSON-serializable representation of the user
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# Set up an event listener to automatically update the 'updated_at' field
@event.listens_for(User, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


