from dotenv import load_dotenv
from pandas import DataFrame

from currency import CurrencyRepository


def main():
    load_dotenv(dotenv_path='envs/.env')
    repo = CurrencyRepository()
    for time_frame in ('15m', '5m', '1m'):
        rows = []
        for row in repo.scrape_currency('BTC/USD', time_frame):
            rows.append(row.dict())
        DataFrame(rows).to_csv(f'BTC_{time_frame}.csv', index=False)


if __name__ == '__main__':
    main()
