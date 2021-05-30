from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from guardian.shortcuts import get_objects_for_user
from .models import Car

# Create your views here.
# @login_required
def index(request):
	username = request.GET['username']
	password = request.GET['password']
	user = authenticate(request, username=username, password=password)
	if user:
		login(request, user)
	else:
		return HttpResponse("Error")
	
	resp = """<!DOCTYPE html>
<html>
	<header></header>
	<body>
    <p>Hello</p>
	</body>
</html>"""
	return HttpResponse(resp)

@login_required
def myCars(request):
	currentUser = User.objects.get(username=request.user.username)
	myCars = get_objects_for_user(currentUser, 'kmrecord.view_car')
	responseStr = 'My cars:\n'
	for car in myCars:
		responseStr += car.licensePlate + '\n'

	return HttpResponse(responseStr)
