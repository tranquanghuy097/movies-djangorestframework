from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from .models import Movie

class MovieTests(APITestCase):
    datalist = [{'name': 'Batman', 'releasedate' : '2021-02-04', 'description' : 'a'},
    {'name': 'b', 'releasedate' : '2021-03-04', 'description' : 'a'},
    {'name': 'c', 'releasedate' : '2022-02-04', 'description' : 'a'},
    {'name': 'd', 'releasedate' : '1997-02-04', 'description' : 'a'}]

    response_ok = status.HTTP_200_OK

    def setUp(self):
        for element in self.datalist:
            Movie.objects.create(**element)

    def test_get_movie(self):
        """
        Ensure we get all movie objects.
        """
        url = reverse('movies-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(response.json()[0]['name'], self.datalist[0]['name'])

    def test_get_movie_by_id(self):
        """
        Ensure we get movie by id.
        """
        url = reverse('movie-id', kwargs={'pk':1})
        response = self.client.get(url)

        self.assertEqual(response.json()['name'], self.datalist[0]['name'])

    def test_create_movie(self):
        """
        Ensure we can create a new movie object.
        """
        url = reverse('movies-list')
        data = {'name': 'Kamen Rider', 'releasedate': '2012-01-01', 'description': 'I am not ok'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.count(), len(self.datalist) + 1)
        self.assertEqual(Movie.objects.get(pk=len(self.datalist) + 1).name, data['name'])

    def test_update_movie(self):
        """
        Ensure we can update movie object.
        """
        data = {'name': 'Kamen Rider', 'releasedate': '2012-01-01', 'description': 'I am not ok'}
        data['name'] = 'abcdef'
        url = reverse('movie-id', kwargs={'pk': 2})
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.get(pk=2).name, data['name'])
        self.assertEqual(Movie.objects.get(pk=2).releasedate.strftime("%Y-%m-%d"), data['releasedate'])
        self.assertEqual(Movie.objects.get(pk=2).description, data['description'])

    def test_delete_movie(self):
        """
        Ensure we can delete movie object.
        """
        url = reverse('movie-id', kwargs={'pk': 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.count(), len(self.datalist) - 1)