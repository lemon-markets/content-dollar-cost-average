from models.Email import Email
from models.Order import Order

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
import os

import time
import telegram_send


class DCA():
    total_price = 0
    total_quantity = 0
    average_price = 0

    def __init__(self, total_pr, total_quant):
        self.total_price = total_pr
        self.total_quantity = total_quant

    def buy_order(self):
        """
        This method places and activates a buy order for 1 unit of the specified instrument every week.
        """
        try:

            placed_order = Order().place_order(
                isin="DE0007664039",
                expires_at="p7d",
                side="buy",
                quantity=3,
            )
            print(placed_order)

            order_id = placed_order['results'].get('id')
            activated_order = Order().activate_order(order_id)
            print(activated_order)

            while True:
                order_summary = Order().get_order(order_id)['results']
                if order_summary.get('status') == 'executed':
                    print('executed')
                    break

            price = order_summary.get('executed_price')
            amount_bought = order_summary.get('executed_quantity')

            self.total_price += price * amount_bought
            self.total_quantity += amount_bought

            self.average_price = self.total_price / self.total_quantity
            Email.send_email(self.average_price / 10000)

            telegram_send.send(messages=[f'Your automated trading strategy just purchased {amount_bought} share(s) '
                                         f'at €{self.average_price / 10000:,.2f} per share.'])

        except Exception as e:
            print(e)


if __name__ == '__main__':

    scheduler = BlockingScheduler(timezone=utc)
    dca = DCA(0, 0)
    scheduler.add_job(dca.buy_order,
                      trigger=CronTrigger(day_of_week="mon-fri",
                                          hour=9,
                                          minute=10,
                                          timezone=utc),
                      name="Perform DCA")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    dca.buy_order()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
