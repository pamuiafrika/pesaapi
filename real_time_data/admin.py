from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('market', 'symbol', 'name', 'current_price', 'previous_close', 'day_range', 'year_range', 'market_cap', 'avg_volume', 'pe_ratio')

