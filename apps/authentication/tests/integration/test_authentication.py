import requests
from django.urls import reverse
from rest_framework.test import APILiveServerTestCase


class UserAuthTest(APILiveServerTestCase):

    def test_email_and_password_registration_already_exists(self):
        email = 'p.e.iusztin.developer@gmail.com'
        password = 'some-pass'

        data = {
            'email': email,
            'password': password
        }

        url = '{}{}'.format(self.live_server_url, reverse('authentication:email-signup'))
        response = requests.post(url, json=data)

        self.assertEqual(response.status_code, 400)

    def test_email_and_password_login(self):
        email = 'p.e.iusztin.developer@gmail.com'
        password = 'some-pass'

        data = {
            'email': email,
            'password': password
        }

        url = '{}{}'.format(self.live_server_url, reverse('authentication:email-login'))
        response = requests.post(url, json=data)

        self.assertEqual(response.status_code, 201)
