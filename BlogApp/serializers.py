from rest_framework import serializers
from .models import BlogPost, Comment, Like, SavedPost, Category, Tag, ContactMessage
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for blog post list (summary)"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'cover_image', 'author',
            'category', 'tags', 'is_published', 'is_featured',
            'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']

    def get_like_count(self, obj):
        return obj.get_like_count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog post detail (full content)"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_saved = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'cover_image', 'cover_image_url', 'author',
            'category', 'tags', 'is_published', 'is_featured',
            'view_count', 'like_count', 'comment_count',
            'user_liked', 'user_saved',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None

    def get_like_count(self, obj):
        return obj.get_like_count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and request.session.session_key:
            return Like.objects.filter(
                post=obj,
                session_id=request.session.session_key
            ).exists()
        return False

    def get_user_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedPost.objects.filter(
                user=request.user,
                post=obj
            ).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'text', 'is_approved', 'created_at']
        read_only_fields = ['is_approved', 'created_at']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text', 'post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'session_id', 'created_at']
        read_only_fields = ['session_id', 'created_at']


class SavedPostSerializer(serializers.ModelSerializer):
    post = BlogPostListSerializer(read_only=True)

    class Meta:
        model = SavedPost
        fields = ['id', 'post', 'saved_at']
        read_only_fields = ['saved_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['is_read', 'created_at']

