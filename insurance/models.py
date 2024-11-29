from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Policy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='policy_images/', null=True, blank=True)
    additional_details = models.TextField(null=True, blank=True)
    default = models.BooleanField(default=False)  # This is the field we're referring to
    created_at = models.DateTimeField(auto_now_add=True)  # Optional, if you need to track creation time

    def __str__(self):
        return self.name

class UserPolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=[('Monthly', 'Monthly'), ('Annual', 'Annual')])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.policy.name}"
