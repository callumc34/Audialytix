from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@sync_to_async
@csrf_exempt
@async_to_sync
async def upload(request, *args, **kwargs):
    return HttpResponse("Request received.")
