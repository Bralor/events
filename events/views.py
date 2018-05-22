from django.http import HttpResponse

# ORIGINAL MESSAGE -> Create your views here.

def index(request):
	return HttpResponse("Hey Client, my app is running!")
