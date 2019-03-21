from rest_framework import serializers
from posts.models import Post, Like


class PostDetailSerializer(serializers.ModelSerializer):

    detail_url = serializers.HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='id'
    )

    like_url = serializers.HyperlinkedIdentityField(
        view_name='posts-api:like',
        lookup_field='id'
    )

    post_author = serializers.CharField(source='owner.username')
    post_like_count = serializers.SerializerMethodField()
    user_liked_post = serializers.SerializerMethodField()

    def get_post_like_count(self, obj):
        return Like.objects.filter(post=obj, is_liked=True).count()

    def get_user_liked_post(self, obj):
        is_liked = False
        try:
            user = self.context.get('request').user
            if user.is_anonymous:
                raise Like.DoesNotExist
            Like.objects.get(post=obj, user=user, is_liked=True)
            is_liked = True
        except Like.DoesNotExist:
            pass
        return is_liked

    class Meta:
        model = Post
        fields = [
            'id',
            'post_author',
            'title',
            'content',
            'timestamp',
            'post_like_count',
            'user_liked_post',
            'image',
            'detail_url',
            'like_url',
        ]


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]


