from django.urls import path
from orders.views import OrderPageView

urlpatterns = [
    path('', OrderPageView.as_view(), name='orderview'),
]
