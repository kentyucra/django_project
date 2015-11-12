from django.http import HttpResponse

def show(request):
    return HttpResponse("Hola Mundo")

