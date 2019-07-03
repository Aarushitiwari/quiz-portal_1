from django.db import models
from events.models import Event
# Create your models here.
class question_model(models.Model):
	question_of_event = models.ForeignKey(Event, on_delete=models.CASCADE)
	question_level=models.IntegerField(unique=True)
	title = models.CharField(max_length=200,null=True)
	description = models.TextField(null=True)
	correct_ans = models.CharField(max_length=500)
	top_level = models.IntegerField(default=15)

	def __str__(self):
		return self.title