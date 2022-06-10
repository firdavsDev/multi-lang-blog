from django.contrib.auth.models import User
from django.db import transaction, utils
from rest_framework import exceptions, serializers, status
from .models import Blog, PostLanguage

# User details
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

#Blogs translates
class PostLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLanguage
        fields = [
            'id',
            'title',
            'content',
            'active',
        ]
        extra_kwargs = {
            'active':{'write_only': True}
        }

#blog serializer
class BlogSerializer(serializers.ModelSerializer):
    post_categories = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='blog_api:blog', lookup_field='pk')
    title_translate = serializers.CharField(allow_blank = True, required = False)
    content_translate = serializers.CharField(allow_blank = True, required = False)
    translate_list = serializers.ListField(write_only=True)
    class Meta:
        model = Blog
        fields = [
            'id',
            'url',
            'author',
            'title',
            'title_translate',
            'content',
            'content_translate',
            'post_categories',
            'categories',
            'image',
            'published_at',
            'views_count',
            'active',
            'slug',
            'translate_list',
            ]
        read_only_fields = ('id','slug', 'post_categories', 'author')
        extra_kwargs = {
            'categories':{'write_only': True},
            'active':{'write_only': True}
        }

    def get_post_categories(self, obj):
        categories = obj.categories.all()
        return [category.name for category in categories]

    def get_author(self, obj):
        return obj.author.username


    def create(self, validated_data):
        translate_list = validated_data.pop('translate_list')
        with transaction.atomic():
            try:
                blog = Blog.objects.create(**validated_data)
                objs = [
                        PostLanguage(
                            post = blog,
                            title = translate['title'],
                            content = translate['content'],
                            language = translate['language'],
                            active = translate['active']
                            )
                        for translate in translate_list
                ]
                PostLanguage.objects.bulk_create(objs)
                # for translate in translate_list:
                #     PostLanguage.objects.create(post=blog, **translate)
            except utils.IntegrityError as e:
                print(e)
                r = exceptions.ValidationError(
                    detail={
                        "error": "Cannot create blog with Blog language",
                    }
                )
                r.status_code = 409
                raise r from e
        return blog
