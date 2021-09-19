from django.urls import path
from accounts.views import RegisterView, LoginView, logout_request

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_request, name="logout"),
]
