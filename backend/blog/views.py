from django.shortcuts import render, get_object_or_404
from blog.models import Blog
from django.utils import timezone


def all_blogs(request):
    blog = Blog.objects.order_by('-date')
    context = {
        'blogs': blog,
        'date': timezone.now
    }
    return render(request, 'blog.html', context=context)


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'detail.html', context=context)
