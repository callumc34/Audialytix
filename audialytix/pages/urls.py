from django.urls import path

from .views import HomePageView, home

urlpatterns = [
    path("", home, name="home")
    # path("", HomePageView.as_view(), name="home"),
]
