from django.urls import path
from .views import (
        BlogAPIView, 
        BlogDetailAPIView,
        )


app_name = 'blog_api'

urlpatterns = [
    path('blogs/', BlogAPIView.as_view(), name='blogs'),
    path('blogs/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog'),

]
