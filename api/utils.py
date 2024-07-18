from django.shortcuts import get_object_or_404
import requests
from bs4 import BeautifulSoup
from rest_framework.exceptions import APIException
from user_agents import parse
from rest_framework.response import Response
from django.utils import timezone
from celery import shared_task

from django.core.mail import send_mail
from .models import RequestLog, Subscription

def quote_currency_result(from_currency: str, to_currency: str):
    try:
        url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            exchange_rate_div = soup.find('div', class_='kf1m0')
            if exchange_rate_div:
                exchange_rate = exchange_rate_div.find('div', class_='YMlKec fxKbKc').text.strip()
                return {"base": from_currency, "target": to_currency, "rate": exchange_rate}
    
        raise APIException("Failed to fetch exchange rates")

    except Exception as e:
        raise APIException(str(e))
    
def convert_currency(from_currency: str, to_currency: str, amount: int):
    try:
        url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            exchange_rate_div = soup.find('div', class_='kf1m0')
            if exchange_rate_div:
                exchange_rate = exchange_rate_div.find('div', class_='YMlKec fxKbKc').text.strip()
                converted_amount = float(amount*exchange_rate.replace(",", ""))
                return {"base": from_currency, "target": to_currency, "amount": amount, "converted_amount": converted_amount, "rate": exchange_rate}
    
        raise APIException("Failed to fetch exchange rates")

    except Exception as e:
        raise APIException(str(e))


def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_os(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    os = user_agent.os.family
    return os

def get_client_browser(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    browser = user_agent.browser.family
    return browser

def log_quote_request(request, user, rate):
    try:
        ip = get_client_ip(request)
        os = get_client_os(request)
        browser = get_client_browser(request)
        base = request.GET.get('base')
        target = request.GET.get('target')
        apikey = request.GET.get('apikey')
        
        RequestLog.objects.create(
            user=user,
            from_currency=base,
            to_currency=target,
            rate=rate,
            browser=browser,
            os=os,
            ip_address=ip,
            isp=apikey,
            country="Unknown"
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)



# @shared_task
# def process_billing():
#     subscriptions_to_bill = Subscription.objects.filter(
#         end_date__gte=timezone.now(),
#         is_paid=False
#     )
#     for subscription in subscriptions_to_bill:
#         subscription.bill_user()

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import User, Subscription

def notify_user_subscription_status(user_id):
    user = get_object_or_404(User, id=user_id)
    subscriptions = Subscription.objects.filter(user=user)

    for subscription in subscriptions:
        if subscription.end_date <= timezone.now():
            status = "expired"
        else:
            status = "active"
        subject = f"Subscription Status Update: {subscription.plan.name} is {status.capitalize()}"
        html_message = render_to_string('emails/subscription_status_email.html', {'user': user, 'subscription': subscription, 'now': timezone.now()})
        plain_message = strip_tags(html_message)  

        mail = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        mail.attach_alternative(html_message, "text/html")
        mail.send()

