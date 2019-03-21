from django.urls import path, re_path
from .views import CreateUserAPIView

app_name = 'users-api'


urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create'),

]
