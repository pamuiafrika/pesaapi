from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    market = models.CharField(max_length=50)
    current_price = models.CharField(max_length=20)
    previous_close = models.CharField(max_length=20)
    day_range = models.CharField(max_length=50)
    year_range = models.CharField(max_length=50)
    market_cap = models.CharField(max_length=20)
    avg_volume = models.CharField(max_length=20)
    pe_ratio = models.CharField(max_length=10)
    dividend_yield = models.CharField(max_length=10)
    primary_exchange = models.CharField(max_length=50)

    def __str__(self):
        return self.symbol
