from models.Order import Order
from models.TradingVenue import TradingVenue

import time
import telegram_send


def buy_order(isin: str):
    """
    This method places and activates a buy order for 1 unit of the specified instrument every week.
    :param isin: isin of the instrument you want to buy
    """
    try:
        placed_order = Order().place_order(
            isin=isin,
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
        time.sleep(604800)  # sleep for a week

    except Exception as e:
        print(e)
        time.sleep(60)


def dollar_cost_averaging():
    while True:
        if TradingVenue().is_open:
            buy_order(
                isin="LU0274208692",  # XTRACKERS MSCI WORLD SWAP
            )
        else:
            time.sleep(TradingVenue().seconds_till_tv_opens())


if __name__ == '__main__':
    dollar_cost_averaging()
