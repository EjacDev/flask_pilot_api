import validators
from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from flaskr.util.utils import response_message
from flaskr.models.service import Rental_service
from flaskr.models.postal_codes import Postal_code
from flask_cors import CORS
from flaskr.util.helper import Helper

bp = Blueprint('service', __name__, url_prefix='/api/service')
CORS(bp)
helper = Helper()

@bp.post('/')
def create_service():
    """Create a new Rental service
    Parameters:
        JSON:
            {
            "zipcode": "01027",
            "latitude": "",
            "longitude": "",
            "user_id": "1"
            }

    Http Codes:
        201: Created
        400: Bad request
        500: Internal server error

    Returns:
        JSON: 
        {
            "message": {
                "created_at": "2022-12-14 18:07:31.845612",
                "id": "14",
                "location": "None",
                "postal_code_id": "3",
                "updated_at": "None",
                "user_id": "1",
                "zipcode_info": {
                    "city": "Easthampton",
                    "country": "USA",
                    "county": "",
                    "created_at": "2022-12-14 17:50:14.920059",
                    "id": "3",
                    "location": "0101000000200c3cf71e3052c0f6285c8fc2254540",
                    "state": "MA",
                    "updated_at": "2022-12-14 18:07:31.849137",
                    "zipcode": "1027"
                }
            },
            "status": "CREATED"
        }
    """
    if request.content_type != 'application/json':
        return response_message('Bad request', 'Content-type must be json type', HTTPStatus.BAD_REQUEST)
    request_data = request.get_json()
    try:
        if not request_data:
            return response_message("message", "Empty request", HTTPStatus.BAD_REQUEST)

        zipcode = str(request_data['zipcode'])
        latitude = request_data.get('latitude','')
        longitude = request_data.get('longitude','')
        user_id = request_data['user_id']

        if  len(zipcode)< 1 and len(zipcode) > 7:
            return response_message('error', "Zip code is  not valid", HTTPStatus.BAD_REQUEST)
        if len(user_id) == 0 :
            return response_message('error', "user_id is not valid", HTTPStatus.BAD_REQUEST)

        #Zip code Processing
        postal_code = Postal_code.get_by_zipcode(zipcode)
        if postal_code is None:
            postal_code = save_zip_code_info(zipcode)
        if postal_code.city == '':
            postal_code = save_zip_code_info(zipcode)

        #Service creation
        if(longitude != '' and latitude != ''):
            geo = f'POINT({longitude} {latitude})'
        else:
            geo = None
        service = Rental_service(
            location = geo,
            postal_code_id = postal_code.id,
            user_id = user_id
        )
        service.save()

        result = service.as_dict()
        result["zipcode_info"] = postal_code.as_dict()
        
        return response_message("CREATED", result, HTTPStatus.CREATED)
    except KeyError as e:
        return response_message('Error', str(e) + ' is missing', HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return response_message('INTERNAL_SERVER_ERROR ', str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

def save_zip_code_info(zipcode):
    zip_code, lat, lng, city, state = helper.get_zipcode_information(zipcode)
    if(lat != '' and lng != ''):
        geo = f'POINT({lng} {lat})'
    else:
        geo = None
    postal_code = Postal_code.get_by_zipcode(zipcode)
    postal_code.zipcode = zip_code,
    postal_code.location = geo,
    postal_code.city = city,
    postal_code.state = state,
    postal_code.county = '',
    postal_code.country = 'USA'
    postal_code.save()
    return postal_code