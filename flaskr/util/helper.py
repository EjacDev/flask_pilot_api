import geopy.distance
import requests, os
from config.settings import Settings
from flaskr.util.utils import print_error, print_success
from flaskr.models import database

class Helper:
    def __init__(self):
        db = database
        
    def get_zipcode_information(self, code: str) -> tuple[str, str, str, str, str]:
        """get the zipcode location information using the zipcode API

        Args:
            zipcode (int): zip code

        Returns:
            zip_code: the original zip code
            lat: latitude in degrees
            lng: longitude in degrees
            city: City name
            state: State abreviation
        """
        try:
            response = requests.get(
                f"{Settings.ZIPCODE_API_URL}{Settings.ZIPCODE_API_KEY}/info.json/{code}/degrees")
            response.raise_for_status()
            data = response.json()
            zip_code = data['zip_code']
            lat = data['lat']
            lng = data['lng']
            city = data['city']
            state = data['state']
            print_success(f"API call successful:{code}")
            return zip_code, lat, lng, city, state
        except ConnectionError as err:
            print_error(str(err))
        except requests.HTTPError as err:
            print_error(str(err))
        except requests.RequestException as identifier:
            print_error(str(identifier))
        return code, str(""), str("") ,str("") ,str("")

    def get_distance(self, point1, point2):
            """
            calculates distance between two latlong values
            :param point1:
            :param point2:
            :return:
            """
            ls = []
            try:
                for i in point1.values():
                    ls.append(i)
                cords_1 = (tuple(ls))
                ls2 = []
                for x in point2.values():
                    ls2.append(x)
                cords_2 = (tuple(ls2))

                return geopy.distance.GeodesicDistance(cords_1, cords_2).km
            except Exception as identifier:
                return 55