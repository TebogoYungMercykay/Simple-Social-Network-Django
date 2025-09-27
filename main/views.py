from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from api.posts.models import Post

@login_required
def home_view(request):
    """
    Display home page with users list and recent posts
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Home page template
    """

    users = User.objects.all().order_by('username')
    recent_posts = Post.objects.all()[:10]
    
    context = {
        'users': users,
        'recent_posts': recent_posts
    }

    return render(request, 'home.html', context)
