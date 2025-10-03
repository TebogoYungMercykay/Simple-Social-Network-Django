from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
from api.posts.models import Post
from django.db.models import Count

@login_required
def home_view(request):
    """
    Display home page with users list and recent posts
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Home page template
    """

    users = User.objects.annotate(
        post_count=Count('posts')
    ).order_by('username')
    
    recent_posts = Post.objects.all()[:10]
    
    context = {
        'users': users,
        'recent_posts': recent_posts
    }

    return render(request, 'home.html', context)
