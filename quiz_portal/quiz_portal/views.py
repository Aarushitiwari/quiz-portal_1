from django.shortcuts import render


def dash(request):
	return render(request,'dashboard.html',{})

def events(request):
	return render(request,'events.html',{})

def leader(request):
	return render(request,'leaderboard.html',{})

def login(request):
	return render(request,'login.html',{})

def signup(request):
	return render(request,'quiz_signup.html',{})

def quiz(request):
	return render(request, 'quiz.html',{})