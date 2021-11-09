"""
 search data from site finance.yahoo.com
"""

import csv
import time
from datetime import datetime

import requests

company_list = ['PD', 'AAPL', 'ZUO', 'PINS', 'ZM', 'DOCU', 'CLDR', 'RUN']

my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.150 Safari/537.36",
    "sec-sh-ua": '"Chromium";v="88", "Google Chrome";v="88", ";Not A '
                 'Brand";v="99"',
    "sec-sh-ua-mobile": '?0',
    'Referer': 'https://www.zooplus.de/'
    }


def page_parser(company, header):
    time_now = int(time.time())
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/" \
          f"{company}?formatted=true&crumb=fVhvGNmVS0h&lang=en-US&region=US" \
          f"&includeAdjustedClose=true&interval=1d&period1=" \
          f"0&period2=" \
          f"{time_now}&events=capitalGain|div|split&useYfid=true&corsDomain" \
          f"=finance.yahoo.com"
    response = requests.get(url=url, headers=header)
    if response.status_code == 200:
        rez = response.json()
        values_list = rez['chart']['result'][0]['indicators']['quote'][0]
        rez_dict = dict()
        for i in range(len(rez['chart']['result'][0]['timestamp'])):
            rez_dict[rez['chart']['result'][0]['timestamp'][i]] = {
                'low': round(values_list['low'][i], 6),
                'close': round(values_list['close'][i], 6),
                'volume': values_list['volume'][i],
                'high': round(values_list['high'][i], 6),
                'open': round(values_list['open'][i], 6),
                'adjclose': round(
                    rez['chart']['result'][0]['indicators']['adjclose'][0][
                        'adjclose'][i], 6
                    )
                }
        return rez_dict
    else:
        return 'bad request'


def csv_parser(company, header):
    time_now = int(time.time())
    url = f'https://query1.finance.yahoo.com/v7/finance/download/' \
          f'{company}?period1' \
          f'=0&period2={time_now}&interval=1d&events=history' \
          f'&includeAdjustedClose=true'

    with requests.Session() as s:
        s.headers.update(header)
        download = s.get(url)
        rez_dict = dict()
        if download.status_code == 200:
            decoded_content = download.content.decode('utf-8')
            csv_r = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(csv_r)
            for row in my_list[1:]:
                rez_dict[datetime.strptime(row[0], '%Y-%m-%d').timestamp()] = {
                    'low': float(row[3]),
                    'close': float(row[4]),
                    'volume': int(row[6]),
                    'high': float(row[2]),
                    'open': float(row[1]),
                    'adjclose': float(row[5])
                    }
        else:
            rez_dict = 'bad request'
    return rez_dict
