from django.http.response import HttpResponse
from django.shortcuts import render
# Create your views here.

def acquire_image(request):

    try:
        with open("media/2015-12-10_0841.jpg", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return HttpResponse("ERROR")
         