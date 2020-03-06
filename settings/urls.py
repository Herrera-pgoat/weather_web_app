from django.urls import path, include 
from django.conf import settings
from . import views

#Here the path is the functions that these url paths are associated with in the views file
#I must implement those functions when I say they are there here
urlpatterns = [
	path('addLocation',views.addLocation,name="addLoc"),
	path('removeLocation',views.removeLocation,name="removeLoc"),
]