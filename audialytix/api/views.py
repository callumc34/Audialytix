import json

import httpx
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import AudioAnalysis


@sync_to_async
def save_audio_model(**kwargs) -> int:
    author = kwargs["author"][0]
    name = kwargs["name"][0]
    analysis_type = "stereo" if kwargs["stereo"][0].casefold() == "true" else "mono"

    entry = AudioAnalysis(
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
        data = {"webhook": webhook}

        # TODO(Callum): Make these changeable in the frontend
        if "onset" in kwargs:
            data["onset"] = json.dumps({"frame_size": "1024", "hop_size": "512"})

        if "spectral" in kwargs:
            data["spectral"] = json.dumps({"frame_size": "1024", "hop_size": "512"})

        return await client.post(url, files=files, data=data)


@sync_to_async
@csrf_exempt
@async_to_sync
async def upload(request, *args, **kwargs):
    analysis_id = await save_audio_model(**request.POST)

    current_host = request.get_host()
    response = await start_analysis(
        analysis_id,
        request.FILES["file"],
        f"http://{current_host}/{settings.WEBHOOKS['results']}",
        **request.POST,
    )

    return HttpResponse("Request received.")
