from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Skill(models.Model):
    skill_name = models.CharField(max_length=20, default="", blank=True)

    def __str__(self):
        return self.skill_name



class project_details(models.Model):
    project_name = models.CharField(max_length=50, default="", blank=False)
    mentor_name = models.CharField(max_length=50, default="", blank=False)
    branch = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=2400)
    paid = models.BooleanField(default=False)
    duration = models.IntegerField(default=6, blank=True)

    def __str__(self):
        return self.project_name + " under " + self.mentor_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50, default="", blank=True)
    year = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=15, default="", blank=True)
    skill_name = models.ManyToManyField(Skill, blank=True)
    # image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.branch + " " + self.year + " " + self.phone


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()









