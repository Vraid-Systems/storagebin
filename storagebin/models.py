from django.db import models

class Binary(models.Model):
    owner = models.ForeignKey('BinOwner', on_delete=models.CASCADE)
    content_key = models.TextField()
    content_type = models.TextField()
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    last_access = models.DateTimeField(null=True)

class BinOwner(models.Model):
    email = models.EmailField()
    key = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
