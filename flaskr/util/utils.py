import pytz
from datetime import datetime
from flask import jsonify

SUCCESS_COLOR = "\033[92m"
ERROR_COLOR = "\033[91m"
END_COLOR = "\033[0m"

def response_message(status, message, status_code):
    """
    method to handle response messages
    """
    return jsonify({
        "status": status,
        "message": message
    }), status_code

def get_service_time():
    service_timezone = pytz.timezone('America/Bogota')
    service_timezone = datetime.now(service_timezone)
    return service_timezone

def print_error(text_error :str):
    print(f"{ERROR_COLOR}{text_error}{END_COLOR}")

def print_success(text:str):
    print(f"{SUCCESS_COLOR}{text}{END_COLOR}")