from django.urls import path

from .views import info, status, upload

urlpatterns = [
    path("upload", upload, name="upload"),
    path("status/<int:id>", status, name="status"),
    path("info/<int:id>", info, name="info"),
]
