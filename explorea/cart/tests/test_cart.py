from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore

# We need import our class 'Cart'
from ..cart import Cart

# Let's write some class with tests
class CartTest(TestCase):

	# we want to set up a few objects
	# that are constantly repeated in 
	# every method
	def set_up(self):
		self.session = SessionStore()
		self.cart = Cart(session)

	# First method is testing if cart has
	# attribute 'session'
	def test_create_cart(self):
		self.assertTrue(hasattr(cart, 'session'))
		self.assertIsInstance(cart.session, SessionStore)
		# Another attribute is instance of a dictionary
		self.assertTrue(hasattr(cart, 'cart'))
		self.assertIsInstance(cart.cart, dict)

	# We want to know if our cart is empty or not
	def test_new_cart_is_empty(self):
		self.assertTrue(cart.is_empty())

	def test_cart_add_item(self):
		product_ID	= '2'
		quantity 	= 1

		cart.add(product_ID=product_ID, quantity=quantity)
		self.assertEqual(session[settings.CART_SESSION_ID][product_ID], 
			cart[product_ID])