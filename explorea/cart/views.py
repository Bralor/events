from django.shortcuts import render
from django.views.generic import TemplateView

# Our first view for testing purposes
# ...
class CartDetailView(TemplateView):
    template_name = "cart/cart_detail.html"