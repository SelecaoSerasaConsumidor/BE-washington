import json
import requests
from order_api.entities import UserEntity


class UserIntegration:

    def __init__(self):
        self.url = 'http://0.0.0.0:8080/user/'

    def validate_user_by_user_id(self, _id):
        r = json.loads(requests.get(self.url + str(_id)).text)
        if 'message' in r:
            return False
        elif 'id' in r:
            return True
