from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from user_detail.models import Profile
#from verify.models import verification
from events.models import Event
from level.models import ParticipantLevel
from questions.models import question_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

User=get_user_model()

def dash(request):
	return render(request,'dashboard.html',{})

def events(request):
	E=Event.objects.all()
	context = {
		'eve':E
	}
	return render(request,'events.html',context)

def leader(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			e_name=request.POST.get('event_name')
			E=Event.objects.filter(event_name=e_name).get()
			participant_list=ParticipantLevel.objects.filter(participant_event=E)
			context={
				"list":participant_list,
				"event_name":e_name
			}
			return render(request,'leaderboard.html',context)
	else:
		return redirect('/login')

def login_page(request):
	if request.user.is_authenticated:
		return redirect('/events')
	else:
		context={
		'login':False
		}
		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')
			user=authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				#pro=Profile.objects.get(username=username)
				return redirect('/events')
		return render(request,'login.html',{})

def signup(request):
	if request.user.is_authenticated:
		return redirect('/events')
	else:
		context={
		"bool":False,
		"exist":False
		}
		if request.method == 'POST':
			username = request.POST.get("username")
			email = request.POST.get("email")
			branch = request.POST.get("branch")
			year = request.POST.get("year")
			college = request.POST.get("college")
			contact_num = request.POST.get("contact")
			password = request.POST.get("password")
			try:
				new_user=User.objects.create_user(
					username=username,
					email=email,
					password=password

					)
			except:
				context['exist']=True
				return render(request,"quiz_signup.html",context)
			new=Profile.objects.create(
				leader=new_user,
				username=username,
				email=email,
				contact_num=contact_num,
				password=password,
				branch=branch,
				year=year,
				college=college
				)
			new.save()
			login(request,new_user)

			return redirect('/events')
		else:
			context = {
				"bool":True
			}

		return render(request,'quiz_signup.html',context)

def quiz(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			e_name=request.POST.get('event_name')
			usr=Profile.objects.get(username=request.user.username)
			E=Event.objects.filter(event_name=e_name).get()
			usr.events.add(E)
			L=ParticipantLevel.objects.filter(participant=usr).filter(participant_event=E)
			if not L:
				new_participant_level=ParticipantLevel.objects.create(
					participant=usr,
					participant_event=E,
					level=1,
					points=0,
					freeze=False,
					lastsub=timezone.now()
					)

			P=ParticipantLevel.objects.filter(participant=usr).filter(participant_event=E).get()
			Q_level=P.level
			try:
				event_question=question_model.objects.filter(question_of_event__event_name=e_name).filter(question_level=Q_level).get()
			except ObjectDoesNotExist:
				return redirect('/')
			if request.POST.get('answer')!=None:
				ans=request.POST.get('answer')
				ans1=event_question.correct_ans
				if (ans.lower())==(ans1.lower()):
					P.level=P.level+1
					P.points=P.points+10
					P.lastsub=timezone.now()
					P.save()
			Q_level=P.level
			try:
				event_question=question_model.objects.filter(question_of_event__event_name=e_name).filter(question_level=Q_level).get()
			except ObjectDoesNotExist:
				return redirect('/')
			context={
				"event_name":e_name,
				"question":event_question,
				"title":event_question.title,
				"description":event_question.description
			}
			return render(request,"quiz.html",context)
	else:
		return redirect('/login')

def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('/')