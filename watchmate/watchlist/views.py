# from re import M
# from django.shortcuts import render
# from django.http import JsonResponse

# from .models import Movie

# # Create your views here.
# def movies_list(request):
#     movies = Movie.objects.all().values()
#     data = {
#         'movies':list(movies)
#         }
#     print(data)
    
#     return JsonResponse(data)


# def movies_detail(request,pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
#     return JsonResponse(data)