from time import time, timezone
from flask import Blueprint, render_template
from .date_form import DateRangeForm
from datetime import datetime, timezone
from .services.coingecko_service import CoinGeckoService

main = Blueprint('main', __name__)
coingecko_service = CoinGeckoService()

@main.route('/', methods=['GET', 'POST'])
def index():
    date_form = DateRangeForm()
    if date_form.is_submitted():

        start_date = date_form.data['start_date']
        end_date = date_form.data['end_date']

        start_timestamp, end_timestamp = dates_to_timestamps(start_date, end_date)
        
        if coingecko_service.ping():
            data = coingecko_service.get_historical_market_data(start_timestamp, end_timestamp)
            daily_prices = coingecko_service.get_daily_prices(data)
            longest_bearish = coingecko_service.get_longest_bearish(daily_prices)

        return render_template('results.html', date_form=date_form, daily_prices=daily_prices, longest_bearish=longest_bearish)

    return render_template('index.html', date_form=date_form)

def dates_to_timestamps(start_date, end_date):
    start_dt = datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone.utc)
    end_dt = datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone.utc)

    return (start_dt.timestamp(), end_dt.timestamp())
