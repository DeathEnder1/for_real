from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Blog1(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=200)
    content=models.TextField()
    image=models.URLField(max_length=200)
    last_update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='Blog'
