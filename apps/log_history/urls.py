
    
    
from django.urls import path
from .views import user_log_list

    
app_name = 'user_history'

urlpatterns = [
         #for routine
        path('user/logs/',user_log_list,name="user_log"),
 
]
