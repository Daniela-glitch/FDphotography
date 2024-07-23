from django.contrib.auth.models import User
from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    caption = models.TextField()
    album = models.ForeignKey('Album', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Blogpost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='')
    content = models.TextField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields if needed
    # bio = models.TextField()  # Remove or add this field as necessary

    def __str__(self):
        return self.user.username


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()