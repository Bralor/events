from django.conf import settings

class Cart:

	# Just 'init' method
	def __init__(self, session):
		self.session = session
		self.cart = session.get(settings.CART_SESSION_ID)

		if not self.cart:
			self.cart = self.session[settings.CART_SESSION_ID] = {}

	# Method which helps us with our cart
	# and its content
	def is_empty(self):
		return len(self.cart) == 0

	# We will add a pair of 'product-ID' and its quantity
	def add(self, product_ID, quantity=1):
		self.cart.update({str(product_ID): quantity})

	# This method will fix the expression
	# cart[item_id]
	def __getitem__(self, item):
		return self.cart[item]