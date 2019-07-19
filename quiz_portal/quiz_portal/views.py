from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from user_detail.models import Profile, OrganiserProfile
from events.models import Event
from level.models import ParticipantLevel
from questions.models import question_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime

User=get_user_model()

def dash(request):
	return render(request,'dashboard.html',{})

def events(request):
	E=Event.objects.all()
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
		if request.user.is_authenticated and org_user.organiser:
			org=True
	except:
		org=False
	now_time = datetime.datetime.now().strftime('%H:%M')
	now_date = datetime.datetime.now().date()

	context = {
		'eve':E,
		'organiser':org,
		#'organiser_name':org_user,
		'now':now_time,
		'now_d':now_date
	}
	return render(request,'events.html',context)

def leader(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
		return redirect('/organiser')
	except:
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
				return redirect('/events')
			else:
				context['login']=True
		return render(request,'login.html',context)

def signup(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
		return redirect('/organiser')
	except:
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
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
		return redirect('/events')
	except:
		if request.user.is_authenticated:
			if request.method == "POST":
				e_name=request.POST.get('event_name')
				if e_name is None:
					return redirect('/events')
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
					context={
					'event_name':e_name,
					}
					return render(request, 'completed.html', context)
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
					context={
					'event_name':e_name,
					}
					return render(request, 'completed.html', context)
				context={
					"event_name":e_name,
					"question":event_question,
					"title":event_question.title,
					"description":event_question.description
				}
				return render(request,"quiz.html",context)
			else:
				return redirect('/events')
		else:
			return redirect('/login')

def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('/')

def org_login_page(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		context={
		'login':False
		}
		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')
			user=authenticate(request,username=username,password=password)
			org_user=OrganiserProfile.objects.filter(organiser_name=username, organiser_password=password)
			if user is not None and org_user is not None:
				login(request,user)
				return redirect('/organiser')
			else:
				context['login']=True
		return render(request,'org_signin.html',context)

def org_dash(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
	except:
		return redirect('/orglogin')
	if request.user.is_authenticated and org_user.organiser:
		events=org_user.organiser_events.all()
		context={
		'event':events
		}
		return render(request, 'OrgDashboard.html', context)
	else:
		return redirect('/')


def org_add_event(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
	except:
		return redirect('/orglogin')
	if request.user.is_authenticated and org_user.organiser:
		context={
		'organiser':True
		}
		if request.method == 'POST':
			e_name=request.POST.get('name')
			e_description=request.POST.get('description')
			temp_start_date=request.POST.get('startdate')
			temp_start_time=request.POST.get('starttime')
			temp_end_date=request.POST.get('enddate')
			temp_end_time=request.POST.get('endtime')
			e_start_date=datetime.datetime.strptime(temp_start_date, "%Y-%m-%d").date()
			e_start_time=datetime.datetime.strptime(temp_start_time, "%H:%M").time()
			e_end_date=datetime.datetime.strptime(temp_end_date, "%Y-%m-%d").date()
			e_end_time=datetime.datetime.strptime(temp_end_time, "%H:%M").time()
			try:
				new_event=Event.objects.create(
					event_name=e_name,
					event_description=e_description,
					event_start_date=e_start_date,
					event_start_time=e_start_time,
					event_end_date=e_end_date,
					event_end_time=e_end_time,
					)
				new_event.save()
			except:
				context={
				'error':True,
				'organiser':True
				}
				return render(request, 'AddEvent.html', context)

			E=Event.objects.filter(event_name=e_name).get()
			org_user.organiser_events.add(E)
			context={
			'event':e_name,
			'organiser':True
			}
			return render(request, 'AddQuestion.html', context)
		return render(request, 'AddEvent.html', context)

def org_add_question(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
	except:
		return redirect('/orglogin')
	if request.user.is_authenticated and org_user.organiser:
		if request.method == 'POST':
			e_name = request.POST.get('eventname')
			if e_name is None:
				context={
				'bool':True
				}
				return render(request, 'AddEvent.html', context)
			E=Event.objects.filter(event_name=e_name).get()
			q_title = request.POST.get('title')
			q_description = request.POST.get('question')
			q_answer = request.POST.get('answer')
			q=question_model.objects.filter(question_of_event__event_name=e_name).all()
			q_level=len(q)+1
			q_top_level=len(q)+1
			try:
				new_question=question_model.objects.create(
					question_of_event=E,
					question_level=q_level,
					title=q_title,
					description=q_description,
					correct_ans=q_answer,
					top_level=q_top_level
					)
				new_question.save()
			except:
				context={
				'error':True
				}
				return render(request, 'OrgDashboard.html', context)
			context={
			'event':e_name
			}
			return render(request, 'AddQuestion.html', context)
		elif request.method == 'GET':
			e_name = request.POST.get('eventname')
			if e_name is None:
				return redirect('/addEvent')



def event_delete(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
	except:
		return redirect('/orglogin')
	if request.user.is_authenticated and org_user.organiser:
		if request.method == 'POST':
			e_name = request.POST.get('eventname')
			if e_name is None:
				return redirect('/organiser')
			instance = Event.objects.filter(event_name=e_name).get()
			instance.delete()
			context={
			'deleted':True
			}
			return redirect('/organiser')




def event_update(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
	except:
		return redirect('/orglogin')
	if request.user.is_authenticated and org_user.organiser:
		if request.method == 'POST':
			e_name = request.POST.get('eventname')
			if e_name is None:
				return redirect('/organiser')

			context={
			'event':e_name,
			'organiser':True
			}
			return render(request, 'AddQuestion.html', context)
	

def contact(request):
	try:
		org_user=OrganiserProfile.objects.get(organiser_name=request.user.username)
		if request.user.is_authenticated and org_user.organiser:
			org=True
	except:
		org=False
	context={
		'organiser':org
	}
	return render(request,'contact.html', context)

def testing(request):
	return render(request,'testing.html',{})