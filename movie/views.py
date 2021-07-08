from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Movie
from .serializer import MovieSerializer

class StatusCode():
    status_ok = status.HTTP_200_OK
    status_not_ok = status.HTTP_400_BAD_REQUEST

# Create your views here.
class ListCreateMovie(ListCreateAPIView):
    model = Movie
    serializer_class = MovieSerializer
    
    def get_queryset(self):
        return Movie.objects.all
    
    def create(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return JsonResponse({
                'message': 'Create successful!'
            }, status=StatusCode.status_ok)

        return JsonResponse({
            'message': 'Create unsuccessful!'
        }, status=StatusCode.status_not_ok)

class RetrieveUpdateDeleteMovieView(RetrieveUpdateDestroyAPIView):
    model = Movie
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, id=kwargs.get('pk'))
        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():
            return JsonResponse(serializer.data, status=StatusCode.status_ok)
        
        return JsonResponse({
                'message': 'Search unsuccessful!'
            }, status=StatusCode.status_not_ok)

    def put(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, id=kwargs.get('pk'))
        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update successful!'
            }, status=StatusCode.status_ok)

        return JsonResponse({
            'message': 'Update unsuccessful!'
        }, status=StatusCode.status_not_ok)

    def delete(self, request, *args, **kwargs):
        car = get_object_or_404(Movie, id=kwargs.get('pk'))
        car.delete()

        return JsonResponse({
            'message': 'Delete successful!'
        }, status=StatusCode.status_ok)

