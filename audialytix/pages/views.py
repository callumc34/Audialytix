from django.views.generic import TemplateView
from django.shortcuts import render
from asgiref.sync import sync_to_async
from .models import AudioFile, OnsetProcessResult, SpectralProcessResult


@sync_to_async
def save_results(audio_name, onset_data, spectral_data):
    audio_file = AudioFile(name=audio_name)
    audio_file.save()

    onset_result = OnsetProcessResult(
        audio_file=audio_file, onset_data=onset_data
    )
    onset_result.save()

    spectral_result = SpectralProcessResult(
        audio_file=audio_file, spectral_data=spectral_data
    )
    spectral_result.save()


async def home(request):
    # Example onset data and spectral data
    onset_data = {"onset_times": [0.1, 0.5, 1.2]}
    spectral_data = {"spectral_features": [0.2, 0.4, 0.6]}

    await save_results("processed_audio.wav", onset_data, spectral_data)

    return render(request, "pages/home.html")


class HomePageView(TemplateView):
    template_name = "pages/home.html"
