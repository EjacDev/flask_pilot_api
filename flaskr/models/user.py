import string
import random
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models.database import db
from flaskr.util.utils import get_service_time

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    middle_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=get_service_time())
    updated_at = db.Column(db.DateTime, onupdate=get_service_time())
    
    service = db.relationship("Rental_service")

    def __repr__(self) -> str:
        return '{self.id}'

    def as_dict(self)-> dict:
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != 'password'}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)\

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()