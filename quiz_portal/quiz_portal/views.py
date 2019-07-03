from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
#from user_detail.models import Profile
#from verify.models import verification


def dash(request):
	return render(request,'dashboard.html',{})

def events(request):
	return render(request,'events.html',{})

def leader(request):
	return render(request,'leaderboard.html',{})

def login_page(request):
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

	return render(request,'quiz_signup.html',{})

def quiz(request):
	return render(request, 'quiz.html',{})