import asyncio
import json
from functools import partial

from api.models import AudioFile, OnsetData, SpectralData
from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@sync_to_async
def update_analysis_results(analysis_id: int, results: dict):
    audio_model = AudioFile.objects.get(id=analysis_id)

    if "onset" in results:
        onset_data = OnsetData(analysis=audio_model, onset_analysis=results["onset"])
        onset_data.save()

    if "spectral" in results:
        spectral_data = SpectralData(
            analysis=audio_model, spectral_analysis=results["spectral"]
        )
        spectral_data.save()


@sync_to_async
@csrf_exempt
@require_POST
@async_to_sync
async def results(request, *args, **kwargs):
    results = json.loads(request.body.decode("utf-8"))
    analysis_id = results["id"]

    task = asyncio.create_task(update_analysis_results(analysis_id, results))

    return HttpResponse("Results received.")
