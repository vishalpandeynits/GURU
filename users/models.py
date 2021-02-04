from django.db import models
from django.contrib.auth.models import User
from basic.models import Classroom
from imagekit.models import ProcessedImageField
from guru.storage_back import PrivateMediaStorage
from imagekit.processors import ResizeToFill

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(default='',max_length=100, null=True, blank=True)
	profile_pic = ProcessedImageField(default='avatar.jpg',upload_to="profile_pics/",storage=PrivateMediaStorage(),
									processors=[ResizeToFill(1000, 1000)],format='JPEG',options={'quality': 100})
	phone_number = models.CharField(max_length=13,null=True,blank=True)
	whatsapp_number = models.CharField(max_length=13,null=True,blank=True)
	pending_invitations = models.ManyToManyField(Classroom)
	
	def __str__(self):
		return f'{self.user.username} Profile'