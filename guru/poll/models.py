from django.db import models
from django.contrib.auth.models import User
import datetime
x = datetime.time()

# Create your models here.
class Poll(models.Model):
	file = models.FileField(upload_to="poll/",null=True,blank = True)
	poll_details = models.TextField(max_length=500)
	created_by = models.ForeignKey(User,related_name="poll_by",on_delete=models.DO_NOTHING)
	voters = models. ManyToManyField(User,related_name="voters")
	announce_at= models.DateTimeField(default=x.strftime("%d-%m-%Y"))

	def __str__(self):
		return self.poll_details

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)



