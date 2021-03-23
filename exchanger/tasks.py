from LMS.settings import EXCHANGE_RATES_SOURCE

from celery import shared_task

from exchanger.models import ExchangeRate

import requests

CURRENCY_MAP = ["USD", "RUR", "EUR"]


@shared_task
def get_exchange_rates():
    resp = requests.get(EXCHANGE_RATES_SOURCE)
    resp = resp.json()
    exchange_rate_update = [get_exchange_rate(d) for d in filter_out_rates(resp)]
    ExchangeRate.objects.bulk_update_or_create(exchange_rate_update, ['currency',
                                                                      'buy',
                                                                      'buy_change',
                                                                      'sell',
                                                                      'sell_change',
                                                                      'created'
                                                                      ], match_field='currency_id')


def filter_out_rates(rates):
    for r in rates:
        currency = r['ccy']
        if currency not in CURRENCY_MAP:
            continue
        yield r


def get_exchange_rate(rate):
    currency_id = rate['ccy'] + rate['base_ccy']
    exchange_rate = ExchangeRate.objects.get(curency_id=currency_id)
    return ExchangeRate(
        currency_id=currency_id,
        currency=rate['ccy'],
        buy=rate['buy'],
        buy_change=get_changes(exchange_rate.buy, rate['buy']),
        sell=rate['sale'],
        sell_change=get_changes(exchange_rate.sell, rate['sale'])
    )


def get_changes(old, new):
    if old - new > 0:
        return -1
    elif old - new < 0:
        return 1
    else:
        return 0
