from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from user_detail.models import Profile
#from verify.models import verification
from events.models import Event
from level.models import ParticipantLevel
from questions.models import question_model


User=get_user_model()

def dash(request):
	return render(request,'dashboard.html',{})

def events(request):
	e=Event.objects.all()
	context = {
		'eve':e
	}
	return render(request,'events.html',context)

def leader(request):
	return render(request,'leaderboard.html',{})

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
				return redirect('/')
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
	return render(request, 'quiz.html',{})

def logout_page(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('/')