import uuid
from django.db import models
from django.contrib.auth.models import User

class Products(models.Model):
    CATEGORY_CHOICES = [
        ('bola biasa', 'Bola Biasa'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('bola luar biasa', 'Bola Luar Biasa'),
        ('kolektor', 'Kolektor'),
        ('signed', 'Signed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def on_click(self):
        self.save()