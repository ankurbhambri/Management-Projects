from django.urls import path
from movies.views import HomePageView, MovieDetails, WhishList, Watched

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('movie/<int:pk>', MovieDetails.as_view(), name='movie'),
    path('whistlist', WhishList.as_view(), name='whistlist'),
    path('watched', Watched.as_view(), name='watched'),
]
