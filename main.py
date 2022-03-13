from models.Order import Order

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
import os

import time
import telegram_send


def buy_order():
    """
    This method places and activates a buy order for 1 unit of the specified instrument every week.
    :param isin: isin of the instrument you want to buy
    """
    try:
        placed_order = Order().place_order(
            isin="LU0274208692",
            expires_at="p0d",
            side="buy",
            quantity=1,
        )

        order_id = placed_order['results'].get('id')
        activated_order = Order().activate_order(order_id)
        print(activated_order)

        while True:
            order_summary = Order().get_order(order_id)['results']
            if order_summary.get('status') == 'executed':
                print('executed')
                break

        average_price = order_summary.get('executed_price')
        amount_bought = order_summary.get('executed_quantity')

        telegram_send.send(messages=[f'Your automated trading strategy just purchased {amount_bought} share(s) '
                                     f'at €{average_price/10000:,.2f} per share.'])

    except Exception as e:
        print(e)

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone=utc)

    scheduler.add_job(buy_order,
                      trigger=CronTrigger(day_of_week="mon-fri",
                                          hour=10,
                                          minute=30,
                                          timezone=utc),
                      name="Perform DCA")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass