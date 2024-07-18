from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from user_agents import parse
from .models import Plan, RequestLog, Subscription
import logging, uuid
from datetime import date, datetime, timedelta
from .utils import convert_currency, get_client_browser, get_client_ip, get_client_os, log_quote_request, notify_user_subscription_status, quote_currency_result
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ForgotPasswordForm, ResetPasswordForm, UserRegistrationForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

from django.utils import timezone
logger = logging.getLogger('django')
User = get_user_model()

from rest_framework.throttling import UserRateThrottle


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([UserRateThrottle]) 
def quote_currency(request):
    try:
        api_key = request.GET.get('apikey')

        if api_key is None or api_key == '':
            raise APIException('API key missing')

        try:
            uuid.UUID(api_key)
        except ValueError:
            return Response({"error": "Invalid API Key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        user = User.objects.filter(api_key=api_key).first()
        if not user:

            raise APIException('Invalid API key')
        
        if not user:
            req_user = user
        else:
            req_user = request.user

        base = request.GET.get('base')
        target = request.GET.get('target')

        result = quote_currency_result(base, target)
        rate_str = result['rate']  
        rate = rate_str.replace('', '')  
        log_quote_request(request, req_user, rate)

        browser = get_client_browser(request)
        ip_address = get_client_ip(request)
        os = get_client_os(request)

        logger.debug(f"User {req_user} converted {base} to {target} at rate {result['rate']} using {browser} on {os} from IP {ip_address}")

        return Response(result)
    except (APIException, ValidationError) as e:
        logger.error(f"Conversion Error: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([UserRateThrottle]) 
def convert_currency(request):
    try:
        api_key = request.GET.get('apikey')

        if api_key is None or api_key == '':
            raise APIException('API key missing')

        try:
            uuid.UUID(api_key)
        except ValueError:
            raise APIException('Invalid API Key')

        user = User.objects.filter(api_key=api_key).first()
        if not user:
            raise APIException('Invalid API key')
        
        if not user:
            req_user = user
        else:
            req_user = request.user

        base = request.GET.get('base')
        target = request.GET.get('target')
        amount = request.GET.get('amount')

        if not amount:
            raise APIException('amount is required')
        
        if not target:
            raise APIException('target currency is required')
        
        if not base:
            raise APIException('base currency is required')

        result = quote_currency_result(base, target)
        rate_str = result['rate']  
        rate = float(rate_str.replace(',', ''))
        converted_amount = float(amount) * rate
        log_quote_request(request, req_user, rate)

        browser = get_client_browser(request)
        ip_address = get_client_ip(request)
        os = get_client_os(request)

        logger.debug(f"User {req_user} converted {base} to {target} at rate {result['rate']} using {browser} on {os} from IP {ip_address}")

        return Response({
            "base": base,
            "target": target,
            "amount": f"{float(amount):,.2f}",
            "converted_amount": f"{converted_amount:,.2f}",
            "rate": f"{rate:,.4f}"
        })
    except (APIException, ValidationError) as e:
        logger.error(f"Conversion Error: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class ConvertCurrencyView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def get(self, request, from_currency, to_currency):
        try:
            conversion_result = quote_currency(from_currency, to_currency)
            
            # Extract user agent info
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            browser = user_agent.browser.family
            os = user_agent.os.family
            
            # Get client IP address
            ip_address = get_client_ip(request)

            # Get ISP and country info using GeoIP2
            isp = country = "Unknown"

            # Log the request in the database
            RequestLog.objects.create(
                user=request.user,
                from_currency=from_currency,
                to_currency=to_currency,
                rate=conversion_result['rate'],
                browser=browser,
                os=os,
                ip_address=ip_address,
                isp=isp,
                country=country
            )

            # Log the request in the log file
            logger.debug(f"User {request.user} converted {from_currency} to {to_currency} at rate {conversion_result['rate']} using {browser} on {os} from IP {ip_address}, ISP {isp}, Country {country}")
            return Response(conversion_result)
        except APIException as e:
            logger.error(f"Conversion error: {e}")
            return Response({"error": str(e)}, status=500)
        



def index(request):
    return render(request, 'index.html')


@login_required
def client_dashboard(request):
    user = request.user
    
    api_requests = RequestLog.objects.all().filter(user=user).order_by('-created_at')[:6]

    context = {
        'api_requests' : api_requests,
        'username' : user,
    }
    return render(request, 'client/index.html', context)  

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_blocked:
                    return render(request, 'authentication/login_blocked.html')

                login(request, user)
                user.reset_login_attempts()  
                return redirect('home') 
            else:
                if User.objects.filter(email=email).exists():
                    existing_user = User.objects.get(email=email)
                    existing_user.login_attempt_failed()

    else:
        form = UserLoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index') 

class ForgotPassword(PasswordResetView):
    form_class = ForgotPasswordForm
    template_name = 'authentication/forgot_password.html'
    success_url = reverse_lazy('password_reset_done')

class ResetPasswordConfirm(PasswordResetConfirmView):
    form_class = ResetPasswordForm
    template_name = 'authentication/reset_password.html'
    success_url = reverse_lazy('password_reset_complete')



@login_required
def plans(request):
    plans = Plan.objects.all()
    return render(request, 'client/plans.html', {'plans': plans})

@login_required
def subscribe(request, plan_id):
    user_id = request.user.id
    plan = Plan.objects.get(id=plan_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, plan=plan)

    if not created:
        subscription.end_date = subscription.start_date + timedelta(days=plan.duration_days)
        subscription.save()
        notify_user_subscription_status(user_id)
        
    else:
        notify_user_subscription_status(user_id)

    return redirect('subscriptions')

@login_required
def subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    for subscription in subscriptions:
        if subscription.is_active:
            # Ensure both are datetime.datetime objects
            end_date = subscription.end_date
            if isinstance(end_date, date) and not isinstance(end_date, datetime):
                end_date = datetime.combine(end_date, datetime.min.time())
            current_datetime = timezone.now()
            days_remaining = (end_date - current_datetime).days
            subscription.days_remaining = days_remaining if days_remaining > 0 else 0
        else:
            subscription.days_remaining = 'N/A'
    return render(request, 'client/subscriptions.html', {'subscriptions': subscriptions})
