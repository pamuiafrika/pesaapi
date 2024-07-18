from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import RequestLog, User

def index(request):
    return render(request, 'index.html')


@login_required
def client_dashboard(request):
    user = request.user
    
    api_requests = RequestLog.objects.all().filter(user=user).order_by('-created_at')[:6]
    username = User.objects.all().filter(email=user).first()
    context = {
        'api_requests' : api_requests,
        'username' : username,
    }
    return render(request, 'client/index.html', context)  

@login_required
def settings_view(request):
    id = request.user.id
    user = User.objects.all().filter(id=id).first()

    context = {
        'usar' : user,
    }

    return render(request, 'profile/settings.html', context)

@login_required
def documentation(request):
    return render(request, 'client/documentation.html', )


@login_required
def support(request):
    return render(request, 'client/support.html', )

