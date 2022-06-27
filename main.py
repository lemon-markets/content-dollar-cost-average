from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from lemon import api
from dotenv import load_dotenv
from pytz import utc
import os

import telegram_send

load_dotenv()
# create your api client with separate trading and market data api tokens
client = api.create(
    trading_api_token=os.environ.get('TRADING_API_KEY'),
    market_data_api_token=os.environ.get('DATA_API_KEY'),
    env='paper'
)


def buy_order():
    """
    This method places and activates a buy order for 1 unit of the specified instrument every week.
    :param isin: isin of the instrument you want to buy
    """
    try:
        placed_order = client.trading.orders.create(
            isin="LU0274208692",
            expires_at=0,
            side="buy",
            quantity=1,
        )

        order_id = placed_order.results.id
        activated_order = client.trading.orders.activate(order_id=order_id)
        print(activated_order)

        while True:
            order_summary = client.trading.orders.get_order(order_id=order_id)
            if order_summary.results.status == 'executed':
                print('executed')
                break

        executed_price = order_summary.results.executed_price
        executed_quantity = order_summary.results.quantity

        telegram_send.send(messages=[f'Your automated trading strategy just purchased {executed_quantity} share(s) '
                                     f'at €{executed_price/10000:,.2f} per share.'])

    except Exception as e:
        print(e)


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=utc)

    scheduler.add_job(buy_order,
                      trigger=CronTrigger(day_of_week="mon-fri",
                                          hour=11,
                                          minute=13,
                                          timezone=utc),
                      name="Perform DCA")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
