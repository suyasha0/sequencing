# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.PositiveSmallIntegerField(blank=True, null=True)
	skintype = models.CharField(max_length=30, default="combination")
	sensitive = models.BooleanField(default=False)

	def __str__(self):
		return "%s %s"%(self.user.first_name,self.user.last_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Product(models.Model):
	name = models.CharField(max_length=255)
	productType = models.CharField(max_length=255)
	url = models.TextField()
	users = models.ManyToManyField(Profile)
