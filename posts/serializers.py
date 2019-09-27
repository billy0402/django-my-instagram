from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Post, Commit


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostCommitSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True)

    class Meta:
        model = Commit
        fields = '__all__'
        read_only_fields = ['id', 'content', 'creator', 'create_at', 'update_at']


class PostSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True)
    commits = PostCommitSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_at', 'update_at']


# class CreatePostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['content']


class CommitSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True)

    class Meta:
        model = Commit
        fields = '__all__'
        read_only_fields = ['id', 'post', 'creator', 'create_at', 'update_at']
