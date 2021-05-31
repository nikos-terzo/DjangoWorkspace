from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from guardian.shortcuts import get_objects_for_user, assign_perm
from .models import Car

# Create your views here.
@login_required
def index(request):
	currentUser = User.objects.get(username=request.user.username)
	context = {}
	context['userCars'] = get_objects_for_user(currentUser, 'kmrecord.view_car')
	return render(request, 'index.html', context)

@login_required
def car(request, licensePlate):
	currentUser = User.objects.get(username=request.user.username)
	carObj = get_object_or_404(Car, licensePlate=licensePlate)
	if not currentUser.has_perm('kmrecord.view_car', carObj):
		return HttpResponseForbidden()
	context = {'car': carObj}
	return render(request, 'car.html', context)

@login_required
def addCar(request):
	currentUser = User.objects.get(username=request.user.username)
	if not currentUser.has_perm('kmrecord.add_car'):
		return HttpResponseForbidden()

	licensePlate = request.POST['licensePlate']
	name = request.POST['name']
	comments = request.POST['comments']
	
	car = Car(licensePlate = licensePlate, name = name, comments = comments)
	car.save()

	assign_perm('kmrecord.view_car', currentUser, car)
	assign_perm('kmrecord.change_car', currentUser, car)
	assign_perm('kmrecord.delete_car', currentUser, car)

	return redirect('kmrecord:index')