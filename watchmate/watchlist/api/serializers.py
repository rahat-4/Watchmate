from rest_framework import serializers

from watchlist.models import WatchList, StreamPlatform, Review

class WatchListSerializer(serializers.ModelSerializer):
    len_title = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList
        fields = "__all__"
        
    def get_len_title(self, object):
        return len(object.title)

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField()
    class Meta:
        model = Review
        exclude = ['watchlist',]