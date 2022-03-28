from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

# Create your views here.
@csrf_exempt
def label_view(request):
    if request.method == 'GET':
        return render(request, "admin_app/label_camera.html")
    if request.method == 'POST':
        response_json = request.body.decode('utf8')
        print(response_json)
        return HttpResponse(status=200)