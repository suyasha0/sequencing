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
	skintype = models.CharField(max_length=30)
	sensitive = models.BooleanField(default=False)

	def __str__(self):
		return "%s %s"%(self.user.first_name,self.user.last_name)


	#hosting = models.ForeignKey(Event, on_delete=models.CASCADE)
	#attending = models.ManyToManyField(Event)
	#tag_history = models.ForeignKey(User_Tag_Record,on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()