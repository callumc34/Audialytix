import json

import httpx
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AudioFile, OnsetData, SpectralData


@sync_to_async
def get_analysis_data(
    model: "OnsetData | SpectralData", analysis_id: int, channel: str, analysis: str
) -> HttpResponse:
    analysis_model = model.objects.get(file=analysis_id)

    if channel not in ["left", "right", "mono"]:
        return HttpResponse("Unknown channel.", status=400)

    if analysis_model.file.is_stereo():
        if channel == "mono":
            return HttpResponse("Channel does not match analysis type.", status=400)
        else:
            if channel not in ["left", "right"]:
                return HttpResponse("Unknown channel.", status=400)
            else:
                analysis = f"{channel}.{analysis}"

    return HttpResponse(json.dumps(analysis_model.data[analysis]), status=200)


async def analysis(request, **kwargs):
    analysis_id = kwargs["id"]
    channel = kwargs["channel"]
    analysis = kwargs["analysis"].replace("_", ".").casefold()

    try:
        if analysis.startswith("onset"):
            return await get_analysis_data(OnsetData, analysis_id, channel, analysis)
        elif analysis.startswith("spectral"):
            return await get_analysis_data(SpectralData, analysis_id, channel, analysis)
        else:
            return HttpResponse("Unknown analysis type.", status=400)

    except Exception as e:
        return HttpResponse("ID not found.", status=400)


@sync_to_async
def save_audio_model(**kwargs) -> int:
    author = kwargs["author"][0]
    name = kwargs["name"][0]
    analysis_type = (
        "stereo" if kwargs["analysis_type"][0].casefold() == "true" else "mono"
    )

    entry = AudioFile(
        author=author,
        name=name,
        analysis_type=analysis_type,
    )
    entry.save()

    return entry.id


async def start_analysis(analysis_id: int, file, webhook, **kwargs):
    async with httpx.AsyncClient() as client:
        url = f"{settings.ANALYSER_HOST}/analyse"
        files = {"file": file}
        data = {
            "webhook": webhook,
            "id": analysis_id,
            "stereo": kwargs["analysis_type"],
        }

        # TODO(Callum): Make frame and hop size changeable in the frontend
        if "onset" in kwargs:
            data["onset"] = json.dumps({"frame_size": "1024", "hop_size": "512"})

        if "spectral" in kwargs:
            data["spectral"] = json.dumps({"frame_size": "1024", "hop_size": "512"})

        if "onset" not in kwargs and "spectral" not in kwargs:
            raise SuspiciousOperation("No analysis type provided.")

        return await client.post(url, files=files, data=data)


@sync_to_async
@csrf_exempt
@require_POST
@async_to_sync
async def upload(request):
    analysis_id = await save_audio_model(**request.POST)

    current_host = request.get_host()
    response = await start_analysis(
        analysis_id,
        request.FILES["file"],
        f"{settings.WEBHOOKS['host']}/{settings.WEBHOOKS['results']}",
        **request.POST,
    )

    return HttpResponse(json.dumps({"id": analysis_id}), status=200)


async def status(request, **kwargs):
    if "id" not in kwargs:
        return HttpResponse("No ID provided.", status=400)

    analysis_id = kwargs["id"]

    try:
        audio_model = await sync_to_async(AudioFile.objects.get)(id=analysis_id)
    except:
        return HttpResponse("ID not found.", status=400)

    response = {}
    failed = await sync_to_async(audio_model.failed)()
    if failed:
        response["status"] = "failed"
        response["error"] = failed
    elif await sync_to_async(audio_model.fulfilled)():
        response["status"] = "fulfilled"
    else:
        response["status"] = "processing"

    return HttpResponse(json.dumps(response), status=200)


async def info(request, **kwargs):
    if "id" not in kwargs:
        return HttpResponse("No ID provided.", status=400)

    analysis_id = kwargs["id"]

    try:
        audio_model = await sync_to_async(AudioFile.objects.get)(id=analysis_id)
    except:
        return HttpResponse("ID not found.", status=400)

    response = {
        "author": audio_model.author,
        "name": audio_model.name,
        "analysis_type": audio_model.analysis_type,
        "analysis_items": await sync_to_async(audio_model.analysis_items)(),
    }
    return HttpResponse(json.dumps(response), status=200)
