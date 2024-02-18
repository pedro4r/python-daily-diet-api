from database import db
from flask_login import UserMixin
import uuid
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
  id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  email = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  meals = relationship("Meal", back_populates="user")