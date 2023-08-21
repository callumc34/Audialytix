from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@sync_to_async
@csrf_exempt
@async_to_sync
async def results(request, *args, **kwargs):
    # TODO(Callum): Results are in request.body
    # Need to be put into the appropriate model
    # Needs the id returned aswell

    return HttpResponse("Results received.")
