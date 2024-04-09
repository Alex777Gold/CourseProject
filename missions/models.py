from django.db import models
from django.contrib.auth.models import User


class Mission(models.Model):
    name = models.CharField(max_length=200)
    launch_date = models.CharField(max_length=200)
    mission_type = models.CharField(max_length=200)
    country = models.CharField(max_length=200)


class MissionDetail(models.Model):
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE)
    youtube_link = models.URLField(max_length=200, null=True, blank=True)
    reddit_link = models.URLField(max_length=200, null=True, blank=True)
    image_link = models.URLField(max_length=200, null=True, blank=True)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
