from django.db import models
from django.utils import timezone
import datetime
from user_detail.models import Profile
from events.models import Event
# Create your models here.
class ParticipantLevel(models.Model):
	participant=models.ForeignKey(Profile, on_delete=models.CASCADE)
	participant_event=models.ForeignKey(Event, on_delete=models.CASCADE)
	level=models.IntegerField(default=1)
	points=models.IntegerField(default=0)
	freeze=models.BooleanField(default=False)
	lastsub=models.DateTimeField(auto_now=False)

	class Meta:
		ordering=['-points','lastsub']
	def __str__(self):
		return self.participant.username+", "+self.participant_event.event_name