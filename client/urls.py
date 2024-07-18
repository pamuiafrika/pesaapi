from django.urls import path
from . import views

from api import views as view

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.client_dashboard, name="home"),
    path('documentation/', views.documentation, name='docs'),
    path('settings/', views.settings_view, name='settings'),
    path('support/', views.support, name='support'),


    path('plans/', view.plans, name='plans'),
    path('subscribe/<int:plan_id>/', view.subscribe, name='subscribe'),
    path('subscriptions/', view.subscriptions, name='subscriptions'),

]
