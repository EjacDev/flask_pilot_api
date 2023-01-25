import validators
from http import HTTPStatus
from flask import Blueprint
from flask import request
from flaskr.util.utils import response_message
from flaskr.models.user import User
from flask_cors import CORS

bp = Blueprint('user', __name__, url_prefix='/api/user')
CORS(bp)


@bp.post('/signup')
def register():
    """Register a new user information

    Parameters:
        JSON:
        {
        "email": "example@gmail.com",
        "first_name": "example",
        "middle_name": "example",
        "last_name": "example",
        "password": "123456"
        }


    Http Codes:
        201: Created
        400: Bad request
        409: Conflict
        500: Internal server error

    Returns:
        JSON: _description_

    """
    if request.content_type != 'application/json':
        return response_message('Bad request', 'Content-type must be json type', HTTPStatus.BAD_REQUEST)
    request_data = request.get_json()
    try:
        if not request_data:
            return response_message("message", "Empty request", HTTPStatus.BAD_REQUEST)

        email= request_data['email']
        first_name= request_data['first_name']
        middle_name= request_data.get('middle_name','')
        last_name= request_data['last_name']
        password= request_data['password']

        if len(password) < 6:
            return response_message('error', "Password is too short", HTTPStatus.BAD_REQUEST)

        if len(first_name) < 1 or len(last_name) <1 :
            return response_message('error', "First Name & Last name are required", HTTPStatus.BAD_REQUEST)

        if not validators.email(email):
            return response_message('error', "Email is not valid", HTTPStatus.BAD_REQUEST)

        if User.get_by_email(email) is not None:
            return response_message('error', "Email is taken", HTTPStatus.CONFLICT)

        # Creamos el usuario y lo guardamos
        user = User(email=email, first_name=first_name,middle_name=middle_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return response_message("CREATED", user.as_dict(), HTTPStatus.CREATED)
    except KeyError as e:
        return response_message('Error', str(e) + ' is missing', HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return response_message('INTERNAL_SERVER_ERROR ', str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

