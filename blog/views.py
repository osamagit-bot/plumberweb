from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    if category:
        posts = posts.filter(category=category)
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    categories = BlogPost.CATEGORY_CHOICES
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'featured_posts': featured_posts,
        'current_category': category,
        'search_query': search,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save(update_fields=['views'])
    
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:3]
    
    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
    })