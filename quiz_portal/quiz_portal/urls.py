"""quiz_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import dash,events,leader,login_page,signup,quiz,logout_page,org_login_page,org_add_event,org_add_question,org_dash,event_delete,event_update,contact,testing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dash),
    path('events/', events),
    path('leaderboard/', leader),
    path('login/', login_page),
    path('signup/', signup),
    path('quiz/', quiz),
    path('logout/', logout_page),
    path('orglogin/', org_login_page),
    path('organiser/', org_dash),
    path('addEvent/', org_add_event),
    path('addQuestion/', org_add_question),
    path('deleteEvent/', event_delete,name='deleteEvent'),
    path('update/', event_update),
    path('contact/', contact),
    path('testing/',testing)
]
