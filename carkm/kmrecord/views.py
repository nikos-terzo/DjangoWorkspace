from django.http.response import HttpResponseForbidden#, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from guardian.shortcuts import get_objects_for_user, assign_perm, get_users_with_perms
from .models import Car, Record, FuelRecord, RichRecord
from decimal import Decimal

# Create your views here.


# Page
@login_required
def index(request):
	user = User.objects.get(username=request.user.username)
	context = {}
	context['cars'] = get_objects_for_user(user, 'kmrecord.view_car')
	return render(request, 'index.html', context)


# Action
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


# Action
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


# Action
@login_required
def deleteCar(request):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=request.POST['licensePlate'])
	if not user.has_perm('kmrecord.delete_car', car):
		return HttpResponseForbidden()

	car.delete()
	return redirect('kmrecord:index')


# Page
@login_required
def car(request, licensePlate):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=licensePlate)
	if not user.has_perm('kmrecord.view_car', car):
		return HttpResponseForbidden()
	
	records = Record.objects.filter(car=car)
	context = {'car': car, 'records': records}
	return render(request, 'car.html', context)


# Action
@login_required
def addRecord(request, licensePlate):
	user = User.objects.get(username=request.user.username)
	car = get_object_or_404(Car, licensePlate=licensePlate)

	if not user.has_perm('kmrecord.change_car', car):	#Maybe adding records shouldn't require changing car
		return HttpResponseForbidden()
	
	record = Record(km=request.POST['km'], date=request.POST['date'])
	record.car = car;
	saved = False

	if 'comments' in request.POST.keys():
		comments = request.POST['comments']
		if comments:
			richRecord = RichRecord(record_ptr=record)
			richRecord.__dict__.update(record.__dict__)
			richRecord.comments = comments
			richRecord.save()

	if {'pricePerLitre', 'price', 'quantity'} <= request.POST.keys():
		pricePerLitre = Decimal(request.POST['pricePerLitre'])
		quantity = Decimal(request.POST['quantity'])
		price = Decimal(request.POST['price'])
		if all (value>0 for value in (pricePerLitre, quantity, price)):
			assert (abs(quantity * pricePerLitre - price)<= 0.01)
			fuelRecord = FuelRecord(record_ptr=record)
			fuelRecord.__dict__.update(record.__dict__)
			fuelRecord.pricePerLitre = pricePerLitre
			fuelRecord.quantity = quantity
			fuelRecord.price = price
			fuelRecord.save()
	
	assign_perm('kmrecord.change_record', user, record)
	assign_perm('kmrecord.delete_record', user, record)
	
	updateUsers = get_users_with_perms(car)
	for user in updateUsers:
		assign_perm('kmrecord.view_record', user, record)

	return redirect('kmrecord:Car', licensePlate=licensePlate)


# Action
@login_required
def changeRecord(request, recordId):
	user = User.objects.get(username=request.user.username)
	record = get_object_or_404(Record, id=recordId)
	if not user.has_perm('kmrecord.change_record', record):
		return HttpResponseForbidden()

	record.km = request.POST['km']
	record.date = request.POST['date']
	record.save()

	# handle comments: If comments exist either change richrecord or create a new
	# else if commments do not exist either remove existinh richrecord or do nothing
	if 'comments' in request.POST.keys():
		comments = request.POST['comments']
		if comments:
			try:
				richRecord = record.richrecord
			except RichRecord.DoesNotExist:
				richRecord = RichRecord(record=record)
				richRecord.__dict__.update(record.__dict__)
			richRecord.comments = comments
			richRecord.save()
			saved = True
		else:
			try:
				richRecord = record.richrecord
				richRecord.delete(keep_parents=True)
			except RichRecord.DoesNotExist:
				pass

	# handle fuel stats: If fuel stats > 0 either change fuelrecord or create a new
	# else if a fuel stat <= 0 delete fuelRecord
	if {'pricePerLitre', 'price', 'quantity'} <= request.POST.keys():
		pricePerLitre = Decimal(request.POST['pricePerLitre'])
		quantity = Decimal(request.POST['quantity'])
		price = Decimal(request.POST['price'])
		if all (value>0 for value in (pricePerLitre, quantity, price)):
			print(request.POST) # debug
			assert (abs(quantity * pricePerLitre - price)<= 0.01)
			try:
				fuelRecord = record.fuelrecord
				print('found!')
			except FuelRecord.DoesNotExist:
				print('creating')
				fuelRecord = FuelRecord(record=record)
				fuelRecord.__dict__.update(record.__dict__)
			fuelRecord.pricePerLitre = pricePerLitre
			fuelRecord.quantity = quantity
			fuelRecord.price = price
			fuelRecord.save()
			saved = True
		else:
			try:
				fuelRecord = record.fuelrecord
				fuelRecord.delete(keep_parents=True)
			except FuelRecord.DoesNotExist:
				pass

	if not saved:
		record.save()
	return redirect('kmrecord:Car', licensePlate=record.car.licensePlate)


# Action
@login_required
def deleteRecord(request, recordId):
	user = User.objects.get(username=request.user.username)
	record = get_object_or_404(Record, id=recordId)
	if not user.has_perm('kmrecord.delete_record', record):
		return HttpResponseForbidden()

	record.delete()
	return redirect('kmrecord:Car', licensePlate=record.car.licensePlate)


# Page
@login_required
def record(request, recordId):
	user = User.objects.get(username=request.user.username)
	record = get_object_or_404(Record, id=recordId)
	if not user.has_perm('kmrecord.view_record', record):
		return HttpResponseForbidden()
	
	context = {'fuelRecord': None, 'comments': ''}
	try:
		fuelRecord = record.fuelrecord
	except FuelRecord.DoesNotExist:
		fuelRecord = FuelRecord(record=record)	# Create it for context but do not save it (yet)
		fuelRecord.__dict__.update(record.__dict__)
	context['fuelRecord'] = fuelRecord

	try:
		richRecord = record.richrecord
		context['comments'] = richRecord.comments # RichRecord only appends a field comments
	except RichRecord.DoesNotExist:
		pass
	return render(request, 'record.html', context)
