from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from guardian.shortcuts import get_objects_for_user, assign_perm
from .models import Car

# Create your views here.
@login_required
def index(request):
	user = User.objects.get(username=request.user.username)
	context = {}
	context['userCars'] = get_objects_for_user(user, 'kmrecord.view_car')
	return render(request, 'index.html', context)

@login_required
def car(request, licensePlate):
	user = User.objects.get(username=request.user.username)
	carObj = get_object_or_404(Car, licensePlate=licensePlate)
	if not user.has_perm('kmrecord.view_car', carObj):
		return HttpResponseForbidden()
	context = {'car': carObj}
	return render(request, 'car.html', context)

@login_required
def addCar(request):
	user = User.objects.get(username=request.user.username)
	if not user.has_perm('kmrecord.add_car'):
		return HttpResponseForbidden()

	licensePlate = request.POST['licensePlate']
	name = request.POST['name']
	comments = request.POST['comments']
	
	car = Car(licensePlate = licensePlate, name = name, comments = comments)
	car.save()

	assign_perm('kmrecord.view_car', user, car)
	assign_perm('kmrecord.change_car', user, car)
	assign_perm('kmrecord.delete_car', user, car)

	return redirect('kmrecord:index')

@login_required
def changeCar(request):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=request.POST['licensePlate'])
	if not user.has_perm('kmrecord.change_car', car):
		return HttpResponseForbidden()

	car.name = request.POST['name']
	car.comments = request.POST['comments']
	car.save()
	return redirect('kmrecord:index')

@login_required
def deleteCar(request):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=request.POST['licensePlate'])
	if not user.has_perm('kmrecord.delete_car', car):
		return HttpResponseForbidden()

	car.delete()
	return redirect('kmrecord:index')