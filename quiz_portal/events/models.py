from django.db import models

# Create your models here.
class Event(models.Model):
	event_name = models.CharField(max_length=100)
	event_description = models.TextField(blank=False)
	event_url = models.URLField(max_length=100,blank=True)

	def __str__(self):
		return self.event_name