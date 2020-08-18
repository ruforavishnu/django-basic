from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.

def homepage(request):
	return render(request=request,
				template_name="main/home.html",
				context={"tutorials": Tutorial.objects.all})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get("username")
			messages.success(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f"Logged in as {username}")

			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
				print(form.error_messages[msg])


	form = NewUserForm
	return render(request=request,
					template_name="main/register.html",
					context={"form": form})


def logout_request(request):
	logout(request)
	messages.info(request, f"Logged out successfully!")
	return redirect("main:login")

def login_request(request):
	if request.method == "POST":	
		form = AuthenticationForm(request=request, data = request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, f"Invalid username or password")
		else:
			messages.error(request, f"Invalid username or password")
					
	else:
		form = AuthenticationForm()
		return render(request, "main/login.html", {"form": form})














