from rest_framework.throttling import UserRateThrottle

class WatchListThrottle(UserRateThrottle):
    scope = "watchlist"
    
class StreamThrottle(UserRateThrottle):
    scope = "stream"