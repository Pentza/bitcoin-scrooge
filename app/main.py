from datetime import datetime, timezone
from flask import Blueprint, render_template, flash
from .date_form import DateRangeForm
from .services.coingecko_service import CoinGeckoService

main = Blueprint('main', __name__)
coingecko_service = CoinGeckoService()

@main.route('/', methods=['GET', 'POST'])
def index():
    date_form = DateRangeForm()
    if date_form.validate_on_submit():

        start_date = date_form.data['start_date']
        end_date = date_form.data['end_date']

        start_timestamp, end_timestamp = dates_to_timestamps(start_date, end_date)

        if coingecko_service.ping():
            data = coingecko_service.get_historical_market_data(start_timestamp, end_timestamp)
            daily_prices = coingecko_service.get_daily_prices(data)
            longest_bearish, price_drop = coingecko_service.get_longest_bearish(data)
            highest_volume = coingecko_service.get_highest_volume(data)

            try:
                graph = coingecko_service.draw_graph(data)
            except Exception: # pylint: disable=W0703
                graph = 'Graph currently unavailable.'

            best_dates = coingecko_service.calculate_best_dates(data)

        return render_template(
            'results.html',
            date_form=date_form,
            daily_prices=daily_prices,
            longest_bearish=(longest_bearish, price_drop),
            highest_volume=highest_volume,
            graph=graph,
            best_dates = best_dates
            )

    flash('Invalid input dates')
    return render_template('index.html', date_form=date_form)

def dates_to_timestamps(start_date, end_date):
    start_dt = datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone.utc)
    end_dt = datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone.utc)

    return (start_dt.timestamp(), end_dt.timestamp())
