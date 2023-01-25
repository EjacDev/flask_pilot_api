import string
import random
from flaskr.models.database import db
from flaskr.util.utils import get_service_time
from geoalchemy2 import Geography

class Rental_service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(Geography(geometry_type='POINT', srid=4326))
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=get_service_time())
    updated_at = db.Column(db.DateTime, onupdate=get_service_time())

    def __repr__(self) -> str:
        return '{self.id}'

    def as_dict(self)-> dict:
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Rental_service.query.get(id)