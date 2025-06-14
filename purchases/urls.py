from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import redirect_view, user_purchases
import os

app_name='purchases'
urlpatterns = [
    path('start/', views.purchase_start_view, name='start'),
    path('success/', views.purchase_success_view, name='success'),
    path('stopped/', views.purchase_stopped_view, name='stopped'),
    path('purchases/', views.user_purchases, name='user_purchases'),
    # path('webhook/', views.my_webhook_view),

]
