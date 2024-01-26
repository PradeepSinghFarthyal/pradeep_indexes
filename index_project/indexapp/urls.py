from django.urls import path
from .admin import *
from .views import IndexListView, DailyPriceListView

urlpatterns = [
    path('indexes/', IndexListView.as_view(), name='index-list'),
    path('daily-prices/<str:index_name>/', DailyPriceListView.as_view(), name='daily-price-list'),
]
