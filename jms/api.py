
from rest_framework import routers
from django.urls import path,include
from apps.log_history.views import UserLogViewSet

router = routers.DefaultRouter()

router.register(r'userlog', UserLogViewSet, 'userlog')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]