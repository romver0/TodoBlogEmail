from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Blog


def all_blogs(request: HttpRequest):
    blog = Blog.objects.order_by('-date')
    context = {
        'blogs': blog,
        'date': timezone.now
    }
    return render(request, 'blog.html', context=context)


def detail(request: HttpRequest, blog_id: int):
    blog = get_object_or_404(Blog, pk=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'detail.html', context=context)
