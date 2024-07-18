import datetime
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        
        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity')
        
        if last_activity:
            elapsed_time = (now - datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')).total_seconds()
            if elapsed_time > settings.SESSION_COOKIE_AGE:
                request.user.auth_token.delete()  # If using Token Authentication
                request.session.flush()
        request.session['last_activity'] = now.strftime('%Y-%m-%d %H:%M:%S')
