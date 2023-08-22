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
    try:
        audio_model = AudioFile.objects.get(id=analysis_id)
    except:
        return

    if "onset" in results:
        onset_data = OnsetData(analysis=audio_model, onset_analysis=results["onset"])
        onset_data.save()

    if "spectral" in results:
        spectral_data = SpectralData(
            analysis=audio_model, spectral_analysis=results["spectral"]
        )
        spectral_data.save()


@sync_to_async
def set_analysis_error(analysis_id: int, error: str):
    try:
        audio_model = AudioFile.objects.get(id=analysis_id)
    except:
        return

    audio_model.error = error
    audio_model.save()


@sync_to_async
@csrf_exempt
@require_POST
@async_to_sync
async def results(request, *args, **kwargs):
    results = json.loads(request.body.decode("utf-8"))
    analysis_id = results["id"]

    if "error" in results:
        asyncio.create_task(set_analysis_error(analysis_id, results["error"]))
        return HttpResponse("Error received.")

    asyncio.create_task(update_analysis_results(analysis_id, results))
    return HttpResponse("Results received.")
