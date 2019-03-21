from django.urls import path, re_path
from .views import PostListAPIView, PostDetailAPIView, PostCreateAPIView, PostLikeAPIView

app_name='posts-api'


urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    re_path(r'(?P<id>[\d]+)/$', PostDetailAPIView.as_view(), name='detail'),
    re_path(r'(?P<id>[\d]+)/like/$', PostLikeAPIView.as_view(), name='like'),
]