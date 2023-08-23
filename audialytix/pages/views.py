from api.models import AudioFile
from asgiref.sync import sync_to_async
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View


class IndexPageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/index.html", context=None)


class HomePageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/home.html", context=None)


class UploadPageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/upload.html", context=None)


class AnalysisPageView(View):
    async def get(self, request, *args, **kwargs):
        if "id" not in request.GET:
            raise SuspiciousOperation("No ID provided.")

        id = request.GET["id"]

        try:
            audio_model = await sync_to_async(AudioFile.objects.get)(id=id)
        except:
            raise SuspiciousOperation("ID not found.")

        if await sync_to_async(audio_model.failed)():
            raise Http404("The requested ID was not found.")
        elif await sync_to_async(audio_model.fulfilled)():
            return render(request, "pages/analysis.html", context={"id": id})
        else:
            return render(
                request, "pages/analysis.html", context={"processing": True, "id": id}
            )
