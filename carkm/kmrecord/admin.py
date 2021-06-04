from django.contrib import admin
from .models import Car, GasStation, Record, RichRecord, FuelRecord
from guardian.admin import GuardedModelAdmin
# Register your models here.


class CarAdmin(GuardedModelAdmin):
	list_display = ('name', 'licensePlate', 'comments')


# Just to see object permissions
class RecordAdmin(GuardedModelAdmin):
	pass


class GasStationAdmin(GuardedModelAdmin):
	pass

admin.site.register(Car, CarAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(GasStation, GasStationAdmin)
admin.site.register(RichRecord)


# TODO: set getters and setters to implement virtual inheritance
class FuelRecordAdmin(GuardedModelAdmin):
	model = FuelRecord
	list_display = ('date', 'km', 'get_car_name', 'get_fuelType',
									'quantity', 'pricePerLitre', 'price', 'gasStation')
	ordering = ('car__name', 'date')

	def get_car_name(self, obj):
		return obj.car.name

	def get_fuelType(self, obj):
		return obj.get_fuelType().name

	get_car_name.short_description = 'Car'
	get_fuelType.short_description = 'Fuel Type'


admin.site.register(FuelRecord, FuelRecordAdmin)
