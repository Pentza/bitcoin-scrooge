from datetime import datetime, timezone
from pycoingecko import CoinGeckoAPI
from collections import defaultdict
import matplotlib.pyplot as plt, mpld3

class CoinGeckoService:
    def __init__(self) -> None:
        self.cg = CoinGeckoAPI()
        self.data = None

    def ping(self):
        if self.cg.ping():
            return True
        return False

    def get_historical_market_data(self, start: str, end: str):
        if not self.ping():
            return None
        
        self.data = self.cg.get_coin_market_chart_range_by_id(
            id = 'bitcoin',
            vs_currency = 'eur',
            from_timestamp = start,
            to_timestamp = end + 3600
            )

        return self.data

    def get_all_prices(self, data):
        prices = defaultdict(list)
        for timestamp, price in data['prices']:
            dt = datetime.fromtimestamp(timestamp/1000, tz=timezone.utc)
            key, _ = str(dt).split()
            value = (dt, price)
            prices[key].append(value)

        return prices

    def get_daily_prices(self, data) -> list:
        all_prices = self.get_all_prices(data)
        dayly_prices = []
        for _, v in all_prices.items():
            daily = min(v, key=lambda x: x[0])
            dayly_prices.append((daily[0], daily[1]))

        return dayly_prices

    def get_longest_bearish(self, data) -> int:
        daily_prices = self.get_daily_prices(data)
        longest = 0
        current = 0
        max_price_drop = 0
        current_price_drop = 0
        for i in range(1, len(daily_prices)):
            if daily_prices[i][1] < daily_prices[i - 1][1]:
                current += 1
                current_price_drop += daily_prices[i - 1][1] - daily_prices[i][1]
            else:
                current = 0
                current_price_drop = 0
            longest = max(current, longest)
            max_price_drop = max(max_price_drop, current_price_drop)
        return longest, max_price_drop

    def get_highest_volume(self, data) -> float:
        d, v = max(data['total_volumes'], key=lambda volume: volume[1])
        d = datetime.fromtimestamp(d/1000, tz=timezone.utc)
        print(d, v)
        return (d, v)

    def draw_graph(self, data):
        data = self.get_all_prices(data)

        x_data = []
        y_data = []
        for k, v in data.items():
            for date, price in v:
                x_data.append(date)
                y_data.append(price)
            
        fig = plt.figure()
        plt.plot(x_data, y_data, 'b-')
        return mpld3.fig_to_html(fig)

    def calculate_best_dates(self, data):
        daily_prices = self.get_daily_prices(data)
        longest_bearish = self.get_longest_bearish(data)

        if (len(daily_prices) - 1) == longest_bearish:
            return (None, None)
        
        buy_date = None
        sell_date = None
        lowest = daily_prices[0]
        current_lowest = daily_prices[0]
        dif = 0

        for daily_price in daily_prices:
            date, price = daily_price

            if price < current_lowest[1]:
                current_lowest = daily_price
            
            dif_to_current_lowest = price - current_lowest[1]

            if dif_to_current_lowest > dif and date > current_lowest[0]:
                dif = dif_to_current_lowest
                sell_date = date
                buy_date = current_lowest[0]

        return (buy_date, sell_date, dif)
