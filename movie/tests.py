from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from .models import Movie

class MovieTests(APITestCase):
    datalist = [{'name': 'a', 'releasedate' : '2021/02/04', 'description' : 'a'},
    {'name': 'b', 'releasedate' : '2021/03/04', 'description' : 'a'},
    {'name': 'c', 'releasedate' : '2022/02/04', 'description' : 'a'},
    {'name': 'd', 'releasedate' : '1997/02/04', 'description' : 'a'}]

    response_ok = status.HTTP_200_OK

    def test_get_movie(self):
        """
        Ensure we get all movie objects.
        """
        for element in self.datalist:
            Movie.objects.create(element)

        url = reverse('movies')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, self.response_ok)
        data_unloaded = json.loads(response.json)
        self.assertEqual(data_unloaded, self.datalist)

    def test_get_movie_by_id(self):
        """
        Ensure we get movie by id.
        """
        for element in self.datalist:
            Movie.objects.create(element)

        url = reverse('movies', kwargs={'pk': 1})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, self.response_ok)
        data_unloaded = json.loads(response.json)
        self.assertEqual(data_unloaded, self.datalist[0])

    def test_create_movie(self):
        """
        Ensure we can create a new movie object.
        """
        index = 0
        url = reverse('movies')
        data = self.datalist[index]
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().name, self.datalist[index]['name'])

    def test_update_movie(self):
        """
        Ensure we can update movie object.
        """
        index = 0
        Movie.objects.create(self.datalist[index])
        data = self.datalist[index]
        data['name'] = 'abcdef'
        url = reverse('movies', kwargs={'pk': 1})
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.get(1).name, data['name'])

    def test_delete_movie(self):
        """
        Ensure we can delete movie object.
        """
        url = reverse('movies')
        data = {'name': 'DabApps', 'releasedate' : '2021/02/04', 'description' : 'a'}
        response = self.client.post(url, data, format='json')
        url = reverse('movies', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, self.response_ok)
        self.assertEqual(Movie.objects.count(), 0)