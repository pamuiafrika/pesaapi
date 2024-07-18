from rest_framework import serializers
from .models import Market, Stock, Forex, Commodity, Cryptocurrency

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forex
        fields = '__all__'

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'
