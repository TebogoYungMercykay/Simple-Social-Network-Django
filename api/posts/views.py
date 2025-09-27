from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post

@login_required
def create_post(request):
    """
    Handle post creation for authenticated users
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Redirect to home page
    """

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Post.objects.create(user=request.user, message=message)
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Post cannot be empty.')
    return redirect('home')

def user_timeline(request, user_id):
    """
    Display user's timeline with all their posts
    
    Args:
        request: Django request object
        user_id: ID of the user whose timeline to display
    
    Returns:
        HttpResponse: User timeline template
    """

    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    context = {
        'profile_user': user,
        'posts': posts,
        'is_own_profile': request.user == user if request.user.is_authenticated else False
    }
    return render(request, 'timeline.html', context)
