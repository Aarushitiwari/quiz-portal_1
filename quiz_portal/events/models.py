from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Event(models.Model):
	event_name = models.CharField(max_length=100, unique=True)
	event_description = models.TextField(blank=False)
	event_url = models.URLField(max_length=100,blank=True)
	event_start_date = models.DateField(default=timezone.now, blank=True)
	event_start_time = models.TimeField(default=datetime.time(00,00), blank=True)
	event_end_date = models.DateField(default=timezone.now, blank=True)
	event_end_time = models.TimeField(default=datetime.time(00,00), blank=True)
	event_num_ques = models.IntegerField(default=0,blank=True)


	def __str__(self):
		return self.event_name