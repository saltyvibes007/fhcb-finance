from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Organization(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    
    def set_password(self, password):
        self.password_hash = make_password(password)
    
    def check_password(self, password):
        return check_password(password, self.password_hash)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']