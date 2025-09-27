from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.posts.models import Post
from api.users.models import UserProfile
from api.utils import sample_posts, users_data
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Create mock users and posts'

    def handle(self, *args, **options):
        created_users = []
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'User already exists: {user.username}')
            
            # Create UserProfile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'is_email_verified': True
                }
            )
            
            if profile_created:
                self.stdout.write(f'Created profile for: {user.username}')
            
            created_users.append(user)

        # Mock posts the 2 Users
        for user in created_users:
            existing_posts = Post.objects.filter(user=user).count()
            posts_to_create = max(0, 5 - existing_posts)
            
            for i in range(posts_to_create):
                days_ago = random.randint(0, 7)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                
                post_time = timezone.now() - timedelta(
                    days=days_ago, 
                    hours=hours_ago, 
                    minutes=minutes_ago
                )
                
                Post.objects.create(
                    user=user,
                    message=random.choice(sample_posts),
                    timestamp=post_time
                )
            
            total_posts = Post.objects.filter(user=user).count()
            self.stdout.write(f'User {user.username} now has {total_posts} posts')

        self.stdout.write(
            self.style.SUCCESS('Successfully created mock data!')
        )
