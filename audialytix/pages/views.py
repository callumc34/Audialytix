from django.shortcuts import render
from django.views import View


class HomePageView(View):
    async def get(self, request, *args, **kwargs):
        return render(request, "pages/home.html", context=None)
