from typing import Any
from flaskr.models.database import db
from flaskr.util.utils import get_service_time
from geoalchemy2 import Geography

class Postal_code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.Integer, unique=True, nullable =False)
    location = db.Column(Geography(geometry_type='POINT', srid=4326))
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    county = db.Column(db.String(40), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=get_service_time())
    updated_at = db.Column(db.DateTime, onupdate=get_service_time())
    
    service = db.relationship("Rental_service")

    def as_dict(self) -> dict:
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def save(self):
        if Postal_code.get_by_zipcode(self.zipcode) is None:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Postal_code.query.get(id)

    @staticmethod
    def get_by_zipcode(zipcode):
        return Postal_code.query.filter_by(zipcode=zipcode).first()