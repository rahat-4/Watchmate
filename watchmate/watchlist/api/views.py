from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist.models import WatchList, StreamPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist.api.throttling import WatchListThrottle, StreamThrottle
from watchlist.api.pagination import WatchPagination, WatchLOPagination, WatchCPagination

from watchlist.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle

class WatchListMV(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [UserRateThrottle]
    # throttle_scope = 'stream'
    # throttle_classes = [WatchListThrottle]
    pagination_class = WatchPagination

# Create your views here.
# class ReviewList(generics.ListAPIView):
#     serializer_class = ReviewSerializer
#     filterset_fields = ['review_user__username', 'comment']
    
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         review = Review.objects.filter(watchlist=pk)
#         return review

class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # filter_backends  = [filters.OrderingFilter]
    # filterset_fields = ['review_user__username', 'comment']
    # ordering_fields = ['rating']
    
    # search_fields = ['review_user__username', 'comment']
    
    # def get_queryset(self):
    #     username = self.kwargs.get('username')
    #     self.request.query_params.get('username')
    #     review = Review.objects.filter(review_user__username=username)
    #     return review
    # def get_queryset(self):
    #     queryset = Review.objects.all()
    #     username = self.request.query_params.get('username')
    #     if username is not None:
    #         queryset = queryset.filter(review_user__username=username)
    #     return queryset
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user, watchlist=movie)
        
        if review_queryset.exists():
            raise ValidationError("User comments already exist.")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        movie.number_rating += 1
        
        movie.save()
        
        serializer.save(watchlist=movie, review_user=review_user)     
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]

class StreamPlatformVS(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [StreamThrottle]
    # throttle_scope = 'stream'
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        # queryset = StreamPlatform.objects.all()
        # stream = get_object_or_404(queryset, pk=pk)
        queryset = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(queryset)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        stream = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    def partial_update(self, request, pk=None):
        stream = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class StreamPlatformAV(APIView):
#     def get(self, request):
#         stream = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(stream, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
# class StreamPlatformDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             stream = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Streamming':'Does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(stream)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         try:
#             stream = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Streamming':'Does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         try:
#             stream = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Streamming':'Does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# class WatchListAV(APIView):
#     def get(self, request):
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()    
#             return Response(serializer.data)
#         return Response(serializer.errors)
        
# class WatchListDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'movie':'Movie does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'movie':'Movie does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)                
        
#     def delete(self, request, pk):
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'movie':'Movie does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)