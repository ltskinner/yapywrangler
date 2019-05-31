
import time
import datetime

import requests

EPOCH_JANUARY_1_2000 = 946684800
EPOCH_ONE_DAY = 86400


def get_yahoo_data(stock_symbol, start_date=None, end_date=None):
    """ Requests and formats data from Yahoo Finance API

    Args:
        start_date: optional, the furthest date back
        end_date: optional, the closest date to now

    Returns:
        dictionary of results
    """

    if start_date is None:
        far_back_time = EPOCH_JANUARY_1_2000
    else:
        far_back_time = convert_date_to_epoch(start_date)

    if end_date is None:
        now_time = int(time.time())
    else:
        now_time = convert_date_to_epoch(end_date)

    url = create_request_url(stock_symbol, far_back_time, now_time)
    response = requests.get(url)

    return unpack_json_to_dict(response.json())


def create_request_url(sym, far_epoch_time, close_epoch_time):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym.upper()
    params = [
        "?formatted=true",
        "lang=en-US",
        "region=US",
        "period1=" + str(far_epoch_time),
        "period2=" + str(close_epoch_time),
        "interval=1d",
        "events=div|split",
        "corsDomain=finance.yahoo.com",
    ]

    return url + "&".join(params)


def unpack_json_to_dict(result_json):
    data = {}

    result = result_json['chart']['result'][0]
    data['timestamp'] = result['timestamp']
    data['date'] = [convert_epoch_to_date(epoch)
                    for epoch in result['timestamp']]

    quote = result['indicators']['quote'][0]
    data['open'] = quote['open']
    data['high'] = quote['high']
    data['low'] = quote['low']
    data['close'] = quote['close']
    data['volume'] = quote['volume']

    return data


def convert_date_to_epoch(date):
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    return int(time.mktime(dt.timetuple()))


def convert_epoch_to_date(epoch):
    return time.strftime('%Y-%m-%d', time.localtime(int(epoch)))
