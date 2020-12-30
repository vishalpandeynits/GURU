from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from basic.models import Classroom

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default='',max_length=100, null=True, blank=True)
	profile_pic = models.ImageField(default='avatar.jpg', upload_to='profile_pics')
	phone_number = models.CharField(max_length=13,null=True,blank=True)
	whatsapp_number = models.CharField(max_length=13,null=True,blank=True)
	pending_invitations = models.ManyToManyField(Classroom)
	
	def __str__(self):
		return f'{self.user.username} Profile'

	def get_absolute_url(self):
		return reverse('profile', kwargs={'username': self.user.username})