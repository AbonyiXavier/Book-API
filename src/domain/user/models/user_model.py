from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, event
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    first_name = db.Column(db.String(345), nullable=False)
    last_name = db.Column(db.String(345), nullable=False)
    email = db.Column(db.String(345), unique=True)
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
    
    # def get_id(self):
    #     return str(self.id)  # Convert user ID to string

    # def is_authenticated(self):
    #     return True  # You can implement your own authentication logic

    # def is_active(self):
    #     return True


# Set up an event listener to automatically update the 'updated_at' field
@event.listens_for(User, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


