from django.contrib import admin

# Register your models here.
from .models import Profile, OrganiserProfile

admin.site.register(Profile)
admin.site.register(OrganiserProfile)