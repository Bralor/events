from django.test import TestCase
from django.urls import resolve, reverse

from ..views import CartDetailView


# this class inherits methods from TestCase
class CartDetailViewTest(TestCase):
	''' Only a temporary solution '''

	# Our first test method will check, that the given URL 
	# for cart detail view resolves to a correct view
	def test_cart_detail_url_resolves_to_cart_detail_view(self):
		page = resolve(reverse('cart:detail'))
		self.assertEqual(page.func.__name__, CartDetailView.__name__)