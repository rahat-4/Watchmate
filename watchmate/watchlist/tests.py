from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from watchlist import models

class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='1mainul23')
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="Netflix popular", website="http://www.netflix.com")
    
    
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Netflix popular",
            "website": "http://www.netflix.com"
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_streamplatform_update(self):
        data = {
            "name": "Netflix - Updated",
            "about": "Netflix popular - Updated",
            "website": "http://www.netflix.com"
        }
        
        response = self.client.patch(reverse('streamplatform-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='1mainul23')
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="Netflix popular", website="http://www.netflix.com")
        self.watch = models.WatchList.objects.create(title="Jon Snow", description="King in the North", platform=self.stream)
        self.watch1 = models.WatchList.objects.create(title="Jon Snow", description="King in the North", platform=self.stream)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, comment="Test is the best", watchlist=self.watch1)
    
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "comment": "Test is the best",
            "watchlist": self.watch,
        }
        
        response = self.client.post(reverse('review-create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 3,
            "comment": "Test is the best - Updated",
            "watchlist": self.watch1,
        }
        
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='1mainul23')
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="Netflix popular", website="http://www.netflix.com")
        self.watch = models.WatchList.objects.create(title="Jon Snow", description="King in the North", platform=self.stream)
    
    def test_watchlist_create(self):
        data = {
            "title": "Jon Snow",
            "description": "King in the North",
            "platform": self.stream,
        }
        
        response = self.client.post(reverse('watchlist-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_watchlist_ind(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_watchlist_update(self):
        data = {
            "title": "Jon Snow - Updated",
            "description": "King in the North",
            "platform": self.stream,
        }
        
        response = self.client.put(reverse('watchlist-detail', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('watchlist-detail', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)