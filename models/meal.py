from database import db
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.user import User

class Meal(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    inside_diet = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = relationship("User", back_populates="meals")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'inside_diet': self.inside_diet,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }