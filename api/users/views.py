from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegisterForm
from api.utils import send_verification_email
from .models import UserProfile
import logging

# auth logger
logger = logging.getLogger('api.users')

@csrf_protect
def register_view(request):
    """
    Handle user registration with email verification
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Registration form or redirect after successful registration
    """

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save new user
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            logger.info(f'New user registered: {username} ({email})')
            
            # Create user profile if it doesn't exist
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'is_email_verified': False}
            )
            
            if created:
                logger.info(f'UserProfile created for {username}')
            
            # Generate verification token
            user_profile.generate_new_verification_token()
            logger.debug(f'Verification token generated for {username}')
            
            # Send verification email using utility
            success, error_message = send_verification_email(request, user_profile)
            
            if success:
                messages.success(
                    request, 
                    f'Account created successfully! Please check your email ({email}) '
                    'and click the verification link to activate your account.'
                )
            else:
                logger.debug(f'Failed Verification: {error_message}')
                messages.error(
                    request, 
                    'Account created but verification email could not be sent. Please contact support.'
                )
            
            return redirect('login')
        else:
            logger.warning(f'Registration form validation failed: {form.errors}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def verify_email(request, token):
    """
    Handle email verification using verification token
    
    Args:
        request: Django request object
        token: Email verification token from URL
    
    Returns:
        HttpResponse: Success redirect or error page
    """

    try:
        user_profile = get_object_or_404(UserProfile, email_verification_token=token)
        username = user_profile.user.username
        
        logger.info(f'Email verification attempt for {username}')
        
        if user_profile.is_verification_token_expired():
            logger.warning(f'Expired verification token used for {username}')
            messages.error(request, 'Verification link has expired. Please request a new verification email.')
            return render(request, 'registration/verification_expired.html', {'user_profile': user_profile})
        
        if user_profile.is_email_verified:
            logger.info(f'Already verified email verification attempt for {username}')
            messages.info(request, 'Your email is already verified. You can log in now.')
            return redirect('login')
        
        # verifying user emaul the user
        user_profile.is_email_verified = True
        user_profile.user.is_active = True
        user_profile.user.save()
        user_profile.save()
        
        logger.info(f'Email successfully verified for {username}')
        messages.success(request, 'Email verified successfully! You can now log in to your account.')
        return redirect('login')
        
    except UserProfile.DoesNotExist:
        logger.warning(f'Invalid verification token used: {token}')
        messages.error(request, 'Invalid verification link.')
        return redirect('register')

def resend_verification_email(request, user_id):
    """
    Resend verification email to user
    
    Args:
        request: Django request object
        user_id: ID of the user profile
    
    Returns:
        HttpResponse: Redirect to appropriate page
    """

    try:
        user_profile = get_object_or_404(UserProfile, id=user_id)
        username = user_profile.user.username
        
        logger.info(f'Resend verification email requested for {username}')
        
        # Check if email is already verified
        if user_profile.is_email_verified:
            logger.info(f'Resend verification requested for already verified user: {username}')
            messages.info(request, 'Your email is already verified.')
            return redirect('login')
        
        # Generate new verification token
        user_profile.generate_new_verification_token()
        logger.debug(f'New verification token generated for {username}')
        
        # Send verification email using utility
        success, error_message = send_verification_email(request, user_profile)
        
        if success:
            messages.success(request, f'Verification email sent to {user_profile.user.email}')
        else:
            messages.error(request, 'Could not send verification email. Please try again later.')
        
        return redirect('login')
        
    except UserProfile.DoesNotExist:
        logger.error(f'Resend verification requested for non-existent user_id: {user_id}')
        messages.error(request, 'User not found.')
        return redirect('register')

@csrf_protect
def login_view(request):
    """
    Handle user authentication with email verification check
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Login form or redirect after successful login
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        logger.debug(f'Login attempt for username: {username}')
        
        try:
            user = User.objects.get(username=username)
            user_profile = user.profile
            
            # user verification checks
            if not user_profile.is_email_verified:
                logger.warning(f'Login attempt with unverified email: {username}')
                messages.error(request, f'Please verify your email address before logging in. Check your email ({user.email}) for the verification link.')
                return render(request, 'registration/login.html', {
                    'show_resend_link': True, 
                    'user_id': user_profile.id,
                    'user_email': user.email
                })
        except User.DoesNotExist:
            logger.debug(f'Login attempt for non-existent user: {username}')
            pass
        except UserProfile.DoesNotExist:
            # create missing user profiles
            try:
                user = User.objects.get(username=username)
                user_profile = UserProfile.objects.create(
                    user=user,
                    is_email_verified=True
                )
                logger.info(f'UserProfile created for existing user: {username}')
            except User.DoesNotExist:
                pass
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                user_profile = user.profile
                if user_profile.is_email_verified:
                    login(request, user)
                    logger.info(f'Successful login: {username}')
                    messages.success(request, f'Welcome back {user.first_name or username}!')
                    return redirect('home')
                else:
                    logger.warning(f'Login blocked - unverified email: {username}')
                    messages.error(request, 'Please verify your email address before logging in.')
            except UserProfile.DoesNotExist:
                # creating a profile for the superuser
                UserProfile.objects.create(
                    user=user,
                    is_email_verified=True
                )
                login(request, user)
                logger.info(f'Successful login with auto-created profile: {username}')
                messages.success(request, f'Welcome back {user.first_name or username}!')
                return redirect('home')
        else:
            logger.warning(f'Failed login attempt: {username}')
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    """
    Handle user logout
    
    Args:
        request: Django request object
    
    Returns:
        HttpResponse: Redirect to login page
    """

    username = request.user.username if request.user.is_authenticated else 'anonymous'
    logout(request)
    logger.info(f'User logged out: {username}')
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')
