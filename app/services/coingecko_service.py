from datetime import datetime, timezone
from pycoingecko import CoinGeckoAPI
from math import floor
from collections import defaultdict

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

        prices = defaultdict(list)
        for timestamp, price in self.data['prices']:
            dt = datetime.fromtimestamp(timestamp/1000, tz=timezone.utc)
            key, _ = str(dt).split()
            value = (dt, price)
            prices[key].append(value)

        return prices

    def get_daily_prices(self, prices: dict) -> list:
        dayly_prices = []

        for _, v in prices.items():
            daily = min(v, key=lambda x: x[0])
            dayly_prices.append((daily[0], daily[1]))

        return dayly_prices

    def get_longest_bearish(self, daily_prices: list) -> int:
        longest = 0
        current = 0
        for i in range(1, len(daily_prices)):
            if daily_prices[i][1] < daily_prices[i - 1][1]:
                current += 1
            else:
                current = 0
            longest = max(current, longest)
        return longest

    def get_highest_volume(self) -> float:
        d, v = max(self.data['total_volumes'])
        d = datetime.fromtimestamp(d/1000, tz=timezone.utc)
        return (str(d), v)


