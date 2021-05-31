from django.urls import path

from . import views

app_name = 'kmrecord'
urlpatterns = [
	path('', views.index, name='index'),
	path('<str:licensePlate>/', views.car, name='car'),
	path('addCar', views.addCar, name='Add Car')
]