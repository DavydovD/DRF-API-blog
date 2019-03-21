from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class ViewTestCase(TestCase):

    def test_api_jwt(self):
        url = reverse('token-auth')
        u = User.objects.create_user(username='Dima', email='user@foo.com', password='04031965')
        u.is_active = False
        u.save()

        resp = self.client.post(url, {'email': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        resp = self.client.post(url, {'username': 'Dima', 'password': '04031965'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        verification_url = reverse('token-verify')
        resp = self.client.post(verification_url, {'token': token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_create(self):
        client = APIClient()
        resp = client.post(
            reverse('users-api:create'),
            {
             "username": "Dima",
             "email": "davidovdima97@gmail.com",
             "password": "123456"
             }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = client.post(
            reverse('users-api:create'),
            {
                "username": "Dima",
                "email": "dfgfdsgsdf@gmail.com",
                "password": "123456"
            }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = client.post(
            reverse('users-api:create'),
            {
                "username": "",
                "email": "davidovdima97@gmail.com",
                "password": "123456"
            }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = client.post(
            reverse('users-api:create'),
            {
                "username": "",
                "email": "",
                "password": "123456"
            }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = client.post(
            reverse('users-api:create'),
            {
                "username": "",
                "email": "davidovdima97@gmail.com",
                "password": ""
            }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

