from django.urls import path

from .views import HomePageView, IndexPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("home", HomePageView.as_view(), name="home"),
]
