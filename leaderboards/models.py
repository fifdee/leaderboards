from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Leaderboard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    private_key = models.CharField(max_length=30)
    public_key = models.CharField(max_length=30)
    modified_date = models.DateTimeField(auto_now=True)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    submitted_date = models.DateTimeField(auto_now_add=True)
