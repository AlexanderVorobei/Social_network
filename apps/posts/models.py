from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=56, null=False, blank=False)
    body = models.TextField(blank=False)
    likes = models.ManyToManyField(User, related_name="likes")
