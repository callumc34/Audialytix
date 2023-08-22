from django.urls import path

from .views import status, upload

urlpatterns = [
    path("upload", upload, name="upload"),
    path("status/<int:id>", status, name="status"),
]
