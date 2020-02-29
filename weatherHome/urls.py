from django.urls import path, include 
from . import views

#Here the path is the functions that these url paths are associated with in the views file
#I must implement those functions when I say they are there here
urlpatterns = [
	path('',views.index, name="index"),
	path('accounts/',include('accounts.urls')),
	path('about', views.about, name="about"),
]