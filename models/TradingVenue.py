import datetime
import os
from helpers import RequestHandler


class TradingVenue(RequestHandler):
    _is_open: bool = False

    @property
    def is_open(self) -> bool:
        mic = os.environ.get("MIC")
        endpoint = f'venues/?mic={mic}'
        response = self.get_data_market(endpoint)
        return response['results'][0].get('is_open', None)

    def check_opening_times(self):
        mic = os.environ.get("MIC")
        endpoint = f'venues/?mic={mic}'
        response = self.get_data_market(endpoint)
        return response

    def seconds_till_tv_opens(self):
        times_venue = self.check_opening_times()
        today = datetime.datetime.today()
        opening_days_venue = times_venue['results'][0].get('opening_days', None)
        next_opening_day = datetime.datetime.strptime(opening_days_venue[0], '%Y-%m-%d')
        next_opening_hour = datetime.datetime.strptime(times_venue['results'][0]['opening_hours'].get('start', None),                                            '%H:%M')
        date_difference = next_opening_day - today
        days = date_difference.days + 1
        if not self.check_if_open():
            print('Trading Venue not open')
            time_delta = datetime.datetime.combine(
                datetime.datetime.now().date() + timedelta(days=1), next_opening_hour.time()
            ) - datetime.datetime.now()
            print(time_delta.seconds + (days * 86400))
            return time_delta.seconds
        else:
            print('Trading Venue is open')
            return 0