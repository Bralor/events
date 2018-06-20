from django.conf import settings


class LoginRequiredMiddleware:
	'''docstring for LoginRequiredMiddleware'''
	
	def __init__(self, get_response):
		print(get_response)
		pass
		