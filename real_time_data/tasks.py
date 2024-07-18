
from celery import shared_task
from .models import Stock
import requests

@shared_task
def update_stock_data(stock_symbol):
    url = f"http://127.0.0.1:8000/api/v1/stock/{stock_symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        stock, created = Stock.objects.update_or_create(
            symbol=data['symbol'],
            defaults={
                'market': data['market'],
                'current_price': data['current_price'],
                'previous_close': data['previous_close'],
                'day_range': data['day_range'],
                'year_range': data['year_range'],
                'market_cap': data['market_cap'],
                'avg_volume': data['avg_volume'],
                'pe_ratio': data['pe_ratio'],
                'dividend_yield': data['dividend_yield'],
                'primary_exchange': data['primary_exchange']
            }
        )

@shared_task
def update_all_stocks():
    stock_symbols = Stock.objects.values_list('symbol', flat=True)
    for symbol in stock_symbols:
        update_stock_data.delay(symbol)

from celery.schedules import crontab
from celery import Celery

app = Celery()

app.conf.beat_schedule = {
    'update-every-minute': {
        'task': 'real_time_data.tasks.update_all_stocks',
        'schedule': crontab(minute='*/1'),
    },
}
