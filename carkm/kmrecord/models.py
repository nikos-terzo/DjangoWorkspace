"""
*********
models.py
*********
"""

from django.db import models
from enum import Enum
from django.utils import timezone
import pytz
from django.contrib.auth.models import User

# Automatic delete of orphaned permissions IMPORTS
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_delete
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission
# Automatic delete of orphaned permissions IMPORTS END

class FuelType(Enum):
	"""
	Fuel types enumerator
	Current choices:

	* GAS - Gas - 0

	* GASOLINE - Gasoline - 1

	* PETROLEUM - Petroleum - 2
	"""
	GAS = 0
	GASOLINE = 1
	PETROLEUM = 2


class Car(models.Model):
	"""
	Defines a car.

	**Attributes**:

	* **licensePlate** - CharField - *required*
		License plate. Also serves as the id field.

	* **name** - CharField - *optional*
		A name for the car. Can be anything.

	"""

	licensePlate = models.CharField(max_length=7, primary_key=True)

	name = models.CharField(max_length=63)

	comments = models.CharField(max_length=255)

	def get_name(self):
		return self.name


class Record(models.Model):
	"""
	Parent for every type of information to record about a car

	**Attributes**:

	* **km** - DecimalField - *optional*
			Kilometers run by the car

	* **createdAt** - DateTimeField - *auto*
			Creation datetime of the object in the database

	* **car** - Car - *required*
			Car referenced in this record
	"""
	km = models.DecimalField(max_digits=9, decimal_places=2)

	date = models.DateTimeField(default=timezone.now())

	car = models.ForeignKey('Car', on_delete=models.PROTECT, null=True, db_column='car_licensePlate')

	# https://django-guardian.readthedocs.io/en/stable/userguide/assign.html#prepare-permissions
	# By default, Django adds 4 permissions for each registered model:
	# add_modelname
	# change_modelname
	# delete_modelname
	# view_modelname (where modelname is a simplified name of our model’s class ).
	# See https://docs.djangoproject.com/en/stable/topics/auth/default/#default-permissions for more detail.)

	# created_by = models.ForeignKey(User, on_delete=models.PROTECT)    #TODO: Test

	# from django.contrib.auth.models import User
	# boss = User.objects.create(username='Big Boss')
	# joe = User.objects.create(username='joe')
	# task = Task.objects.create(summary='Some job', content='', reported_by=boss)
	# joe.has_perm('assign_task', task)                             # add/change/delete/view?
	# False

	def get_car(self):
		return self.car

	def get_km(self):
		return self.km

	def get_date(self):
		return self.date


class RichRecord(Record):
	"""
	Record with extra information
	**Attributes**:

	* **date** - DateTimeField - *optional*
		An extra date the user wants to add (on top of the creation date). For whatever reason.

	* **comments** - CharField - *optional*
		Comments about the record
	"""
	# record = models.ForeignKey('Record', on_delete=models.PROTECT, primary_key=True, db_column='record_id')

	comments = models.CharField(max_length=255)


# Example store a FuelRecord
# frec = FuelRecord(record = recs[0], type=FuelType.GASOLINE.value, price=15.,quantity=10.,pricePerLitre=1.5,gasStation='Shell mhden')
class FuelRecord(Record):
	"""
	Recording fuel fills
	**Attributes**:

	* **type** - FuelType - *required*
		Fuel type of fill. Current choices:

		#. GAS

		#. GASOLINE

		#. PETROLEUM

	* **Price Quantity PricePerLitre** triplet. Obviously the three values below are dependent but all are stored to track round-off errors
		* **price** - Decimal - *required*
			Price paid for the fuel

		* **quantity** - Decimal - *required*
			Quantity of fuel filled

		* **pricePerLitre** - Decimal - *required*
			Price per litre.
	"""
	# record = models.ForeignKey('Record', on_delete=models.PROTECT, primary_key=True, db_column='record_id')

	fuelType = models.SmallIntegerField()

	price = models.DecimalField(max_digits=5, decimal_places=2)

	quantity = models.DecimalField(max_digits=7, decimal_places=3)

	pricePerLitre = models.DecimalField(max_digits=5, decimal_places=3)

	gasStation = models.CharField(max_length=63)

	"""
	Returns the fuel type of the FuelRecord
	Returns: **type** - FuelType(Enum)
	"""

	def get_fuelType(self):
		return FuelType(self.fuelType)

	"""
	Sets the fuel type of the FuelRecord
	:arg **type** - FuelType(enum)
	"""

	def set_fueltype(self, type):
		self.fuelType = type.value

	# def get_record(self):
	#     return self.record
	#
	# #TODO: Test also date, ...
	# def get_car(self):
	# 	return self.record.car


# Automatic delete of orphaned permissions
def remove_obj_perms_connected_with_obj(sender, instance, **kwargs):
	filters = Q(content_type=ContentType.objects.get_for_model(instance),
			object_pk=instance.pk)
	UserObjectPermission.objects.filter(filters).delete()
	GroupObjectPermission.objects.filter(filters).delete()

pre_delete.connect(remove_obj_perms_connected_with_obj, sender=Car)
pre_delete.connect(remove_obj_perms_connected_with_obj, sender=Record)