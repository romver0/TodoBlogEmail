from rest_framework import viewsets, permissions
from blog.serializer import BlogSerializer
from blog.models import Blog


class BlogViewSet(viewsets.ModelViewSet):
    blogs = Blog.objects.order_by('-date')
    queryset = Blog.objects.order_by('-date')
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser]
