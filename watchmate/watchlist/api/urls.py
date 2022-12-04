from django.urls import path, include
from watchlist.api.views import *

from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('list/', movies_list,name='movies-list'),
#     path('<int:pk>/', movies_detail,name='movies-detail')
# ]

router = DefaultRouter()
router.register(r'stream', StreamPlatformVS, basename='streamplatform')
router.register(r'list', WatchListMV, basename='watchlist')

urlpatterns = [
    # path('watchlist/', WatchListAV.as_view(),name='watchlist'),
    # path('watchlist/<int:pk>/', WatchListDetailAV.as_view(),name='watchlist-detail'),
    
    path('', include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(),name='stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(),name='stream-detail'),
    
    path('<int:pk>/review/', ReviewList.as_view(),name='review-list'),
    # path('<int:pk>/review/<str:username>/', ReviewList.as_view(),name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(),name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(),name='review-detail')
]