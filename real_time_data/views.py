import logging
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.throttling import UserRateThrottle

from api.models import User
from .engine import scrape_crypto_data, scrape_stock_data
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.decorators import permission_classes, throttle_classes

logger = logging.getLogger('django')

class StockDataLiveAPIView(APIView):
    permission_classes([AllowAny])
    throttle_classes([UserRateThrottle])

    def get(self, request):
        try:
            api_key = request.GET.get('apikey')
            symbol = request.GET.get('symbol')

            if api_key is None or api_key == '':
                raise APIException('API key is missing')

            if symbol is None or symbol == '':
                raise APIException('Symbol is missing')
            
            try:
                uuid.UUID(api_key)
            except ValueError:
                return Response({"error": "Invalid API Key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user = User.objects.filter(api_key=api_key).first()

            if not user:
                raise APIException('Invalid API key')


            market = "NASDAQ"
            data = scrape_stock_data(symbol, market)
            return Response(data, status=status.HTTP_200_OK) 
        except (APIException, ValidationError) as e:
            logger.error(f"Stock Conversion Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CryptoDataLiveAPIView(APIView):
    permission_classes([AllowAny])
    throttle_classes([UserRateThrottle])

    def get(self, request):
        try:
            api_key = request.GET.get('apikey')
            symbol = request.GET.get('symbol')

            if api_key is None or api_key == '':
                raise APIException('API key is missing')

            if symbol is None or symbol == '':
                raise APIException('Symbol is missing')
            
            try:
                uuid.UUID(api_key)
            except ValueError:
                return Response({"error": "Invalid API Key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user = User.objects.filter(api_key=api_key).first()

            if not user:
                raise APIException('Invalid API key')
            
            data = scrape_crypto_data(symbol)
            return Response(data, status=status.HTTP_200_OK)
        except (APIException, ValidationError) as e:
            logger.error(f"Crypto Conversion Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
