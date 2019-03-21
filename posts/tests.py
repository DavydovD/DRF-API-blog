from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Like


# Create your tests here.

class ViewTestCase(TestCase):

    def setUp(self):
        url = reverse('token-auth')
        self.u = User.objects.create_user(username='Dima', email='user@foo.com', password='04031965')
        resp = self.client.post(url, {'username': 'Dima', 'password': '04031965'}, format='json')
        self.p = Post.objects.create(title='test case title', content='test case content')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.token = resp.data['token']
        self.client = APIClient()

    def test_get_posts(self):
        resp = self.client.get(reverse('posts-api:list'), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_post(self):

        client = self.client

        resp = self.client.post(reverse('posts-api:create'), {'title': 'testing', 'content': 'test pass'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        resp = client.post(reverse('posts-api:create'), {'title': 'testing', 'content': 'test pass'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = client.post(reverse('posts-api:create'), {'title': 'testing'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_detail_test(self):
        resp = self.client.get(reverse('posts-api:detail', kwargs={'id': '1'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(reverse('posts-api:detail', kwargs={'id': '211'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_like_test(self):
        client = self.client

        resp = self.client.post(reverse('posts-api:like', kwargs={'id': '1'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.post(reverse('posts-api:like', kwargs={'id': '1'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        l = Like.objects.get(post=self.p, user=self.u)
        self.assertEqual(l.is_liked, True)

        resp = self.client.post(reverse('posts-api:like', kwargs={'id': '1'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        l = Like.objects.get(post=self.p, user=self.u)
        self.assertEqual(l.is_liked, False)

        resp = self.client.post(reverse('posts-api:like', kwargs={'id': '211'}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)




