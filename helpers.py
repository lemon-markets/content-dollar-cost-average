import os
import requests
import json
from dotenv import load_dotenv


class RequestHandler:

    def __init__(self):
        load_dotenv()
        self.headers = {'Authorization': 'Bearer ' + os.environ.get('API_KEY')}
        self.url_trading: str = os.environ.get("BASE_URL_TRADING")
        self.url_market: str = os.environ.get("BASE_URL_DATA")

    def get_data_trading(self, endpoint: str):
        response = requests.get(self.url_trading + endpoint, headers=self.headers)
        return response.json()

    def get_data_market(self, endpoint: str):
        response = requests.get(self.url_market + endpoint, headers=self.headers)
        return response.json()

    def post_data(self, endpoint: str, data):
        response = requests.post(self.url_trading + endpoint, json.dumps(data), headers=self.headers)
        return response.json()
