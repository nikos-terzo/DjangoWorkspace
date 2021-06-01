from django.urls import path

from . import views

app_name = 'kmrecord'
urlpatterns = [
	path('', views.index, name='index'),
	path('<str:licensePlate>/', views.car, name='car'),	# temp
	path('addCar', views.addCar, name='Add Car'),
	path('changeCar', views.changeCar, name='Change Car'),
	path('deleteCar', views.deleteCar, name='Delete Car')
]