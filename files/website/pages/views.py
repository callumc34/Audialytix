from api.models import AudioFile
from asgiref.sync import sync_to_async
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View


class IndexPageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/index.html", context=None)


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get("search", None)

        audio_files = AudioFile.objects.all()
        if search:
            audio_files = audio_files.filter(
                name__icontains=search
            ) | audio_files.filter(author__icontains=search)

        audio_files = [file for file in audio_files if file.fulfilled()]

        # 30th is upload card
        paginator = Paginator(audio_files, 15)

        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        try:
            page_number = int(page_number)
        except:
            raise Http404("Page not found.")

        if page_number > paginator.num_pages:
            raise Http404("Page not found.")

        return render(request, "pages/home.html", {"page_obj": page_obj})


class UploadPageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/upload.html", context=None)


class AnalysisPageView(View):
    async def get(self, request, *args, **kwargs):
        if "id" not in request.GET:
            raise SuspiciousOperation("No ID provided.")

        analysis_id = request.GET.get("id")

        try:
            audio_model = await sync_to_async(AudioFile.objects.get)(id=analysis_id)
        except:
            raise SuspiciousOperation("ID not found.")

        if await sync_to_async(audio_model.failed)():
            raise Http404("The requested ID was not found.")
        elif await sync_to_async(audio_model.fulfilled)():
            return render(request, "pages/analysis.html", context={"id": analysis_id})
        else:
            return render(
                request,
                "pages/analysis.html",
                context={"processing": True, "id": analysis_id},
            )
