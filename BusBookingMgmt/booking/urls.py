from django.urls import path
# from booking import views
from booking.views import (HomePageView, BookingListView,
                           CheckoutView, SucessView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('booking', BookingListView.as_view(), name='booking'),
    path('booking/<slug:slug>/', CheckoutView.as_view(), name='bookingview'),
    path('success', SucessView.as_view(), name='success'),
]
