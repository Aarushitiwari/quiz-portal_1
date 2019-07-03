from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
User = get_user_model()
# Create your models here.
class Profile(models.Model):
	leader=models.ForeignKey(User,on_delete=models.CASCADE)
	username=models.CharField(max_length=100)
	email=models.EmailField()
	contact_num=models.IntegerField()
	events=models.ManyToManyField(Event, blank=True)
	password=models.CharField(max_length=100,null=False,blank=False)
	branch=models.CharField(max_length=50,blank=False)
	year=models.IntegerField()
	college=models.CharField(max_length=100,blank=False)

	def __str__(self):
		return self.username