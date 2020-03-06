from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
import pandas as pd
import requests 
import os 
import hashlib


# Create your models here.
#The class below is called weather
# i have currently deleted everything in the table for weather
class weather(models.Model):
	#this is the date of when we got the weather. We should keep this
	dateOfWeather = models.DateTimeField(default=datetime.now)
	#From the api we get weather in kalvin but we will convert to fahrenheit when we go here
	#maybe celsius too idk. That can be an option 
	temperature = models.DecimalField(max_digits = 4, decimal_places = 1, default =0 )
	temperatureFeel = models.DecimalField(max_digits = 4, decimal_places = 1, default = 0)
	#speed is meters/second
	wind = models.DecimalField(max_digits = 3,decimal_places = 1,default = 0)
	#rain volume in mm
	rain = models.DecimalField(max_digits = 5 , decimal_places = 2, default=0 )
	#This is how much it is snowing in mm ? 
	snow = models.DecimalField(max_digits = 5 , decimal_places = 2, default=0 )
	#This city code is from the json file citylist and with the city code I can get the weather accurately for the city they want
	cityCode = models.CharField(max_length = 30,primary_key = True, null=False) # I would like this to be the primary key but maybe it shouldn't be
	#This will be the zipcode that the place is located. Gives kinda easy access to get the weather from api. But I should have very easy access from the key
	zipcode = models.CharField(max_length = 10, null=False)
	#Getting the city they are requesting data from
	cityName = models.CharField(max_length = 100, null=False)
	#Getting the state that they are requesting data from. This information may be superfluous but I will get it anyway
	#I get it from asking useres to fill out form they want to get data from 
	stateName = models.CharField(max_length = 200, null=False)
	#The country that this city and or state is in.
	countryName = models.CharField(max_length = 200, null=False)


	def within_fifteen_min(self):
		#"Returns Whether we this information is within the past 15 minutes
		import datetime
		#what this is doing is we are adding 15 minutes to the last time we got the date of the weather
		#then we are checking the current time and chcecking if we are past the 15 minutes
		#if 15 minutes have past we return false
		#otherwise we return true 
		time_threshold = self.dateOfWeather + datetime.timedelta(minutes=15)
		currentTime = timezone.now()#datetime.datetime.now(USE_TZ=False)
		print (currentTime)
		print (time_threshold)
		if currentTime > time_threshold:
			return False
		else:
			return True
			
	def __str__(self):
		return str(self.cityName) + " " + str(self.stateName) + " " +  str(self.countryName)
		
#This model is called user and it has attributes that we want the user table to hold
#IT SEEMS LIKE I CAN'T SWAP THE USER MODEL MIDWAY THROUGH PRODUCTION OF A DJANGO APPLICATION SO I WILL HAVE TO USE THE DEFAULT ONE
#NEXT PROJECT I AM USING MY OWN USER MODEL AND IT WILL INCLUDE SOMETHING THE OLD ONE DOESN'T 	
class user(models.Model):
	#Everything here in the user stuff is unaffected by our decision to go with weather thing api
	username = models.CharField(max_length = 50, primary_key = True, null=False)#I would like this to be the primary key but maybe it should't be 
	userEmail = models.CharField(max_length = 50, null=False)
	userFirstName = models.CharField(max_length = 30, null=False)
	userLastName = models.CharField(max_length = 30, null=False)
	passwordHashed = models.CharField(max_length = 2048, null=False)
	passwordSalt = models.CharField(max_length= 1024, null=False)
	dateAccountCreated = models.DateTimeField(default=datetime.now())
	
	def encryptString(passwordPreHash,salt):
	#creating the salt using a random thing I think
		#using an encryption algorithm to save the password safely
		#documentation https://docs.python.org/3/library/hashlib.html on the function below 
		passwordHashed = hashlib.pbkdf2_hmac('sha256',passwordPreHash.encode(),salt,1000 )
		return passwordHashed
	
	def createSalt():
		return os.urandom(128)
		
	def __str__(self):
		return self.username

#This is the weatherForUsers table that will connect which weather stations a user has connected to 
#When either the weather station or the user is deleted the delete will cascade here making sure 
#We don't hold empty space. The cascading delete is possible because we are using a foreign key 
class weatherForUsers(models.Model):
	#AUTH_USER_MODEL is the user model that is being used right now. I don't need to define it. The one that is being used is the django default one :(
	username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) #both of these are foreign keys
	#Right here this will change, it will still be a foreign key to the weather key or something but 
	#it is now an id rather than identifying a station 
	cityCode = models.ForeignKey('weather', on_delete = models.CASCADE) # both of these are foreign keys
	
	#This is a method that says what we return if we want the model as a string and it returns the username are returning the user name
	def __str__(self):
		return (self.username.__str__() + self.cityCode.__str__())
		
class countryAndCode(models.Model):
	countryName = models.CharField(max_length = 100) # both of these are foreign keys
	twoCharCountryCode = models.CharField(max_length = 2) # both of these are foreign keys
	
	def __str__ (self):
		return self.countryName
		
		