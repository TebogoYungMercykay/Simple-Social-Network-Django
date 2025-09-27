from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    def is_verification_token_expired(self):
        if self.email_verification_sent_at:
            expiration_time = self.email_verification_sent_at + timedelta(hours=24)
            return timezone.now() > expiration_time
        return True
    
    def generate_new_verification_token(self):
        self.email_verification_token = uuid.uuid4()
        self.email_verification_sent_at = timezone.now()
        self.save()
