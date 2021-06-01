from django.http.response import HttpResponseForbidden#, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from guardian.shortcuts import get_objects_for_user, assign_perm, get_users_with_perms
from .models import Car, Record


# Create your views here.
@login_required
def index(request):
	user = User.objects.get(username=request.user.username)
	context = {}
	context['cars'] = get_objects_for_user(user, 'kmrecord.view_car')
	return render(request, 'index.html', context)


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

	return redirect('kmrecord:cars')


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


@login_required
def car(request, licensePlate):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=licensePlate)
	if not user.has_perm('kmrecord.view_car', car):
		return HttpResponseForbidden()
	
	records = Record.objects.filter(car=car)
	context = {'car': car, 'records': records}
	return render(request, 'car.html', context)


@login_required
def addRecord(request, licensePlate):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=licensePlate)

	if not user.has_perm('kmrecord.change_car', car):	#Maybe adding records shouldn't require changing car
		return HttpResponseForbidden()
	
	record = Record(km=request.POST['km'], date=request.POST['date'])
	record.car = car;
	record.save()
	assign_perm('kmrecord.change_record', user, record)
	assign_perm('kmrecord.delete_record', user, record)
	
	updateUsers = get_users_with_perms(car)
	for user in updateUsers:
		assign_perm('kmrecord.view_record', user, record)

	return redirect('kmrecord:Car', licensePlate=licensePlate)


@login_required
def changeRecord(request, recordId):
	user = User.objects.get(username=request.user.username)
	record = get_object_or_404(Record, id=recordId)
	if not user.has_perm('kmrecord.change_record', record):
		return HttpResponseForbidden()

	record.km = request.POST['km']
	record.date = request.POST['date']
	record.save()
	return redirect('kmrecord:Car', licensePlate=record.car.licensePlate)


@login_required
def deleteRecord(request, recordId):
	user = User.objects.get(username=request.user.username)
	record = get_object_or_404(Record, id=recordId)
	if not user.has_perm('kmrecord.delete_record', record):
		return HttpResponseForbidden()

	record.delete()
	return redirect('kmrecord:Car', licensePlate=record.car.licensePlate)


@login_required
def record(request, recordId):
		# user = User.objects.get(username=request.user.username)
	# carObj = get_object_or_404(Car, licensePlate=licensePlate)
	# if not user.has_perm('kmrecord.view_car', carObj):
	# 	return HttpResponseForbidden()
	
	# records = Record.objects.filter(car=carObj)
	# context = {'car': carObj, 'records': records}
	# return render(request, 'car.html', context)
	return redirect('kmrecord:index')