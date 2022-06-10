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

    # def create(self, request, *args, **kwargs):
    #     r = request.data
    #     title = r['title']
    #     content = r['content']
    #     active = r['active']
    #     translate_list = r['translate_list']
    #     with transaction.atomic():
    #         try:
    #             blog = Blog.objects.create(title=title, content=content, active=active, author=request.user)
    #             for translate in translate_list:
    #                 PostLanguage.objects.create(post=blog, title=translate['title'], content=translate['content'], active=translate['active'])
    #         except utils.IntegrityError as e:
    #             print(e)
    #             r = exceptions.ValidationError(
    #                 detail={
    #                     "error": "Cannot create blog with Blog language",
    #                 }
    #             )
    #             r.status_code = 409
    #             raise r from e
    #     return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)

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
