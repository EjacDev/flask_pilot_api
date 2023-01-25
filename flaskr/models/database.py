from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_database(app):
    db.init_app(app)

    from flaskr.models.user import User
    from flaskr.models.service import Rental_service
    from flaskr.models.postal_codes import Postal_code

    with app.app_context():
        db.create_all()
        
        