from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    pass


class Leaderboard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    private_key = models.CharField(max_length=50)
    public_key = models.CharField(max_length=50)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Score(models.Model):
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    points = models.IntegerField()
    time = models.CharField(max_length=20, null=True)
    submitted_date = models.DateTimeField()
    extra = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name}: {self.points}'


class Feedback(models.Model):
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f'{self.email}: {self.message}'


def update_modified(sender, instance, **kwargs):
    leaderboard = Leaderboard.objects.get(pk=instance.leaderboard.pk)
    leaderboard.modified_date = now()
    leaderboard.save()


def set_username(sender, instance, **kwargs):
    email = instance.email
    username = email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username


post_save.connect(update_modified, sender=Score)
pre_save.connect(set_username, sender=User)
