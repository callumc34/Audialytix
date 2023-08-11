from django.urls import path

from .views import HomePageView, IndexPageView, UploadPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("home", HomePageView.as_view(), name="home"),
    path("upload", UploadPageView.as_view(), name="upload"),
]
