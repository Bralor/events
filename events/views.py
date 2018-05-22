from django.http import HttpResponse

# ORIGINAL MESSAGE -> Create your views here.

# def index(request):
# 	return HttpResponse("Hey Client, my app is running!")

def event_listing(request):
	html = '''
	
	<ul>
		<li> Chill on the beach </li>
		<li> Camping in the woods </li>
		<li> Flying into the space </li>
	</ul>
	'''
	return HttpResponse(html)

def index(request):
	html = '''

	<h1> Hey Client, my app si actually running! </h1>
	<p> Check out our <a href="/events">offerings </a>

	'''
	return HttpResponse(html)
