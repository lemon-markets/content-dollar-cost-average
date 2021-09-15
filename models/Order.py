import os
from dotenv import load_dotenv
from helpers import RequestHandler


class Order(RequestHandler):

    def place_order(self, isin: str, valid_until: float, quantity: int, side: str):
        order_details = {
            "isin": isin,
            "valid_until": valid_until,
            "side": side,
            "quantity": quantity,
        }
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/'
        response = self.post_data(endpoint, order_details)
        return response

    def activate_order(self, order_uuid):
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/{order_uuid}/activate/'
        response = self.put_data(endpoint)
        return response

    def get_order(self, order_uuid):
        load_dotenv()
        space_uuid = os.getenv("SPACE_UUID")
        endpoint = f'spaces/{space_uuid}/orders/{order_uuid}/'
        response = self.get_data_trading(endpoint)
        return response

