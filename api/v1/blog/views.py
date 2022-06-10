from asyncio.log import logger
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.v1.blog.permissions import IsAuthorOrReadOnly
from .models import Blog, PostLanguage
from .serializers import BlogSerializer
from api.v1.blog.utils import clean_query_data
from rest_framework.response import Response
from django.db import transaction, utils
from rest_framework import exceptions, serializers, status

#list blog
class BlogAPIView(ListCreateAPIView):
    queryset = Blog.custom_objects.get_published_blogs()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queries = clean_query_data(self.request.query_params)
        return Blog.custom_objects.get_translate_blog_list(queries)


#Detail blog
class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.custom_objects.get_published_blogs()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'pk'

    def get_queryset(self):
        queries = clean_query_data(self.request.query_params)
        return Blog.custom_objects.get_translate_blog_detail(blog_pk=self.kwargs.get('pk'), queries=queries)
