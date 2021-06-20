from collections import defaultdict
from datetime import datetime
import json
from multiprocessing.pool import ThreadPool

import pandas as pd
import numpy as np

from main import collect_data, add_indicators


def find_oversold_and_overbought():
    file = 'data/BTC_1m.csv'
    df = add_indicators(pd.read_csv(file))
    open_time = df.open_time
    rsi = df.rsi

    history = defaultdict(list)
    last = None
    for o, r in zip(open_time, rsi):
        if np.isnan(r):
            continue

        if r > 80 or r < 20:
            if last and (datetime.fromisoformat(o) - datetime.fromisoformat(last)).seconds / 60 < 4:
                continue
            last = o
            history[o.split(' ')[0]].append(o)

    counts = [len(i) for i in history.values()]
    print('Average per day: ', sum(counts) / len(counts))

    def calculate_profit(minute):
        x = 20
        price = 10
        profit = 0
        for index, day in enumerate(history.values()):
            if index % 100 == 0:
                print(f'{minute} {index}/{len(history.values())}')
            for item in day:
                row = df.loc[df.open_time == item].iloc[0]
                start = row.close
                end = df.iloc[row.name + minute].close
                diff = (start - end) * (x * price / row.close) - 0.25
                profit += diff
        return f'{minute} minute: {profit}'

    results = ThreadPool(15).map(calculate_profit, range(1, 16))
    for r in results:
        print(r)

    with open('oversold_and_overbought.json', 'w') as f:
        json.dump(history, f, indent=2)


if __name__ == '__main__':
    # collect_data()
    find_oversold_and_overbought()
