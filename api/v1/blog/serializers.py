from django.contrib.auth.models import User
from requests import request
from rest_framework import serializers

from .models import Blog, PostLanguage


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class BlogSerializer(serializers.ModelSerializer):
    post_categories = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='blog_api:blog', lookup_field='pk')

    class Meta:
        model = Blog
        fields = [
            'url',
            'author',
            'title',
            'content',
            'post_categories',
            'categories',
            'image',
            'published_at',
            'views_count',
            'active',
            'slug'
            ]
        read_only_fields = ('slug', 'post_categories', 'author')
        extra_kwargs = {
            'categories':{'write_only': True},
            'active':{'write_only': True}
        }

    def get_post_categories(self, obj):
        categories = obj.categories.all()
        return [category.name for category in categories]

    def get_author(self, obj):
        return obj.author.username

class BlogDetailSerializer(serializers.ModelSerializer):
    post_categories = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'author',
            'title',
            'content',
            'post_categories',
            'categories',
            'image',
            'published_at',
            'views_count',
            'active',
            'slug',
            ]
        read_only_fields = ('slug', 'post_categories', 'author')
        extra_kwargs = {
            'categories':{'write_only': True},
            'active':{'write_only': True}
        }

    def get_post_categories(self, obj):
        categories = obj.categories.all()
        return [category.name for category in categories]

    def get_author(self, obj):
        return obj.author.username


class PostDetailLanguageSerializer(serializers.ModelSerializer):
    post = BlogSerializer(read_only=True)
    class Meta:
        model = PostLanguage
        fields = [
            'post',
            'title',
            'content',
            'categories',
            'active',
            ]
        read_only_fields = ('slug', )
        extra_kwargs = {
            'categories':{'write_only': True},
            'active':{'write_only': True}
        }
