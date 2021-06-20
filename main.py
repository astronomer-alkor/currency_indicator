import os
from datetime import datetime, timedelta

import pandas as pd
import ta
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from pandas import DataFrame

from currency import CurrencyRepository

load_dotenv(dotenv_path='envs/.env')


def collect_data(latest=False):
    repo = CurrencyRepository()
    if latest:
        path = 'latest_data'
        latest_date = datetime.utcnow() - timedelta(hours=8)
    else:
        path = 'data'
        latest_date = None
    for time_frame in ('5m', '1m'):
        df = DataFrame(repo.scrape_currency('BTC/USD', time_frame, latest_date))
        df.iloc[::-1].to_csv(f'{path}/BTC_{time_frame}.csv', index=False)


def add_indicators(df):
    rsi = ta.momentum.RSIIndicator(df.close)

    df['rsi'] = rsi.rsi()

    return df


def visualization():
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 14)
    ax.set_facecolor('#1d111d')
    ax.grid(color='#2f242f', linewidth=3)
    ax.set_xticklabels([])
    ax.tick_params(axis='both', which='major', labelsize=40, colors='w', bottom=False)
    plt.axhline(y=30, color='w', linestyle='--', linewidth=2)
    plt.axhline(y=70, color='w', linestyle='--', linewidth=2)
    plt.ylim((10, 90))
    plt.xlim(datetime.utcnow() - timedelta(hours=1), datetime.utcnow())

    colors = ('#62286b', '#0000ff')
    for file, color in zip(os.listdir('latest_data'), colors):
        file = os.path.join('latest_data', file)
        df = pd.read_csv(file)

        open_time = [
            datetime.fromisoformat(i) for i in df.open_time
            if datetime.fromisoformat(i) > datetime.utcnow() - timedelta(hours=1)
        ]
        rsi = df.rsi[-len(open_time):].tolist()

        plt.plot(open_time, rsi, color, linewidth=8)

    plt.savefig(
        'rsi.png',
        bbox_inches='tight',
        pad_inches=0,
        transparent=False
    )


if __name__ == '__main__':
    collect_data()
    add_indicators()
    visualization()
