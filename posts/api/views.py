from .serializers import PostDetailSerializer, PostCreateSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.models import Post, Like
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView


class PostListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDetailAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'


class PostCreateAPIView(CreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostCreateSerializer
        permission_classes = (IsAuthenticated,)
        lookup_field = 'id'

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)
            return Response(status.HTTP_201_CREATED)


class PostLikeAPIView(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request, id):
            post = get_object_or_404(Post, id=id)
            user = request.user
            try:
                like = Like.objects.get(post=post, user=user)
                if like.is_liked:
                    like.is_liked = False
                    like.save()
                    return Response(status=status.HTTP_200_OK)
                like.is_liked = True
                like.save()
                return Response(status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                Like.objects.create(post=post, user=user, is_liked=True)
                return Response(status=status.HTTP_200_OK)



