import urllib
from datetime import datetime
from typing import Generator, List, Optional

import requests

from config import CurrencyConfig
from entities import Currency

time_frames = {
    '1m': 60000,
    '5m': 300000,
    '15m': 900000,
    '30m': 1800000,
    '1h': 3600000,
    '4h': 14400000,
    '1d': 86400000,
    '1w': 604800000
}


class CurrencyRepository:
    def __init__(self):
        self.url = CurrencyConfig().api_url

    def get_available_tickers(self):
        data = requests.get(f'{self.url}ticker/24hr').json()
        return {item['symbol'] for item in data}

    def scrape_currency(
            self,
            ticker: str,
            time_frame: str,
            latest_date: Optional[datetime] = None
    ) -> Generator[Currency, None, None]:

        collected_items_times = set()
        prepared_symbol = urllib.parse.quote(ticker)
        start_time_prepared = ''

        offset = 20 if latest_date else 900

        while True:
            tmp_url = f'{self.url}klines?symbol={prepared_symbol}&interval={time_frame}&limit=1000{start_time_prepared}'
            response = requests.get(tmp_url)
            if response.status_code != 200:
                break

            chunk = []
            for item in reversed(response.json()):
                item[0] = datetime.utcfromtimestamp(item[0] // 1000)
                if latest_date and item[0] <= latest_date:
                    break
                if item[0] in collected_items_times:
                    continue
                collected_items_times.add(item[0])
                item = Currency(
                    ticker=ticker,
                    open_time=item[0],
                    open=item[1],
                    close=item[2],
                    high=item[3],
                    low=item[4],
                    volume=item[5],
                    time_frame=time_frame
                ).dict()
                chunk.append(item)

            if chunk:
                yield from chunk
            else:
                break

            start_time = int(chunk[-1]['open_time'].timestamp()) * 1000 - time_frames[time_frame] * offset
            start_time_prepared = '&startTime=' + str(start_time)
            offset = 900
