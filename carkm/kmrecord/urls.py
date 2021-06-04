from django.urls import path

from . import views

app_name = 'kmrecord'
urlpatterns = [
	path('', views.index, name='Cars'),
	path('cars/', views.index, name='Cars'),
	path('cars/index', views.index, name='Cars'),
	path('cars/addCar', views.addCar, name='Add Car'),
	path('cars/changeCar', views.changeCar, name='Change Car'),
	path('cars/deleteCar', views.deleteCar, name='Delete Car'),
	path('cars/<str:licensePlate>/', views.car, name='Car'),	# temp
	path('cars/<str:licensePlate>/addRecord', views.addRecord, name='Add Record'),
	path('cars/<str:licensePlate>/createRecord', views.createRecord, name='Create Record'),
	path('records/<int:recordId>/changeRecord', views.changeRecord, name='Change Record'),
	path('records/<int:recordId>/deleteRecord', views.deleteRecord, name='Delete Record'),
	path('records/<int:recordId>/', views.record, name='Record')
]