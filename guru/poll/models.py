from django.db import models
from django.contrib.auth.models import User
import datetime
x = datetime.time()
from basic.models import Classroom

# Create your models here.
class Poll(models.Model):
	choices = [('All Members',"All Members"),('Students','Students')]
	classroom = models.ForeignKey(Classroom,on_delete= models.CASCADE)
	file = models.FileField(upload_to="poll/",null=True,blank = True)
	poll_details = models.TextField(max_length=500)
	created_by = models.ForeignKey(User,related_name="poll_by",on_delete=models.DO_NOTHING)
	who_can_vote = models.CharField(choices=choices,max_length=30,default='Students')
	voters = models. ManyToManyField(User,related_name="voters")
	announce_at= models.DateTimeField()

	def __str__(self):
		return self.poll_details

class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text