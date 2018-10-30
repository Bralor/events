# What we need for this .py file
import time
from django.test import LiveServerTestCase
from django.urls import reverse

# Webdriver for Firefox?
from selenium import webdriver


class AnonymousUserTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome('C:/Users/Matous/_python/_online_degree/explorea/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_anonymous_user(self):
        # New visitor enters the url of detail_view into
        # the browser
        self.browser.get(self.live_server_url + reverse('cart:detail'))
        time.sleep(5)

        # She sees the detail page announcing there is nothing
        # in the shopping cart
        self.assertIn('Cart Detail', self.browser.title)

        # The visitor decides to go to the events page where
        # she selects the first event available
        events_link = self.browser.find_element_by_css_selector('#nav-buttons a:first-of-type')
        events_link.click()

        # Visitor is taken to the events page
        self.assertIn('Event Listing', self.browser.title)