from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    # Дополнительные поля, такие как дата производства, срок годности, производитель и т.д.
    
    def __str__(self):
        return self.name

class ScanHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} scanned {self.product.name} on {self.scan_date}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(default=5)
    review_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} on {self.product.name}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    is_gpt = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = RichTextField()
    photo = models.FileField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]