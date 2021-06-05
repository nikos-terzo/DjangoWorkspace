from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'kmrecord'
urlpatterns = [
	path('', RedirectView.as_view(url='cars/')),
	path('cars/', views.cars, name='Cars'),
	path('cars/addCar', views.addCar, name='Add Car'),
	path('cars/<str:licensePlate>/changeCar', views.changeCar, name='Change Car'),
	path('cars/<str:licensePlate>/deleteCar', views.deleteCar, name='Delete Car'),
	path('cars/<str:licensePlate>/', views.car, name='Car'),	# temp
	path('cars/<str:licensePlate>/addRecord', views.addRecord, name='Add Record'),
	path('cars/<str:licensePlate>/createRecord', views.createRecord, name='Create Record'),
	path('records/<int:recordId>/changeRecord', views.changeRecord, name='Change Record'),
	path('records/<int:recordId>/deleteRecord', views.deleteRecord, name='Delete Record'),
	path('records/<int:recordId>/', views.record, name='Record'),
	path('gasstations/', views.gasStations, name='GasStations'),
	path('gasstations/addGasStation', views.addGasStation, name='Add GasStation'),
	path('gasstations/<int:gasStationId>/changeGasStation', views.changeGasStation, name='Change GasStation'),
	path('gasstations/<int:gasStationId>/deleteGasStation', views.deleteGasStation, name='Delete GasStation')
]