from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup as soup
from .models import weather, weatherForUsers
from datetime import datetime
#this import is from a file I wrote to do certain things that made this file too complicated. Visit that file for more details
from .weatherFunctions import weatherCityInfo
import json
import requests

# Create your views here.
#Function Name: index
#Every time we get a request for the home page we go through this whole function
#What this function is going to do right now is check if the data we have is within the most 15 minutes of recent data 
#and then if it is we return that data and if it is not we do not return that data but instead get new updated data 
def index(request):

	#If you are logged in then I will show you weather of everysingle thing you have aksed for
	if request.user.is_authenticated:
		currentUser = request.user	
		
		#getting all rows that this user is in 
		userToWeatherTieList = weatherForUsers.objects.filter(username = currentUser)
		
		#now for each row that the user is in I want to get a list of all the weather stuff they are tied to 
		weatherInfoList = list()
		
		for singleTie in userToWeatherTieList:
			#adding each weather info stuff to the list
			weatherInfoList.append(singleTie.cityCode)
		
		#for each thing in the weatherInfolist I should check if it is updated right then get the new information from the database?
		for oneCityWeather in weatherInfoList:
			#calling a function that returns a dictionary with relevent information about weather
			apiLink = "https://api.openweathermap.org/data/2.5/weather?id={}&appid=e11569a6d5c1f254fa71baae792905e1"
			weatherInfo = weatherCityInfo ( oneCityWeather.cityCode, apiLink)
			currWeather = weather.objects.get(cityCode = oneCityWeather.cityCode)
			#filling some variables with information about the current weather from the weatherInfo dictionary 
			realTemperature = weatherInfo['realTemperature']
			feelTemperature = weatherInfo['feelTemperature']
			snowNow = weatherInfo['snowNow']
			rainNow = weatherInfo['rainNow']
			windNow = weatherInfo['windNow']
			now = weatherInfo['timeNow']
				
			#I got the currweather object above when I got the city with a certain id
			#now I am giving it updated data
			currWeather.dateOfWeather = now
			currWeather.rain = rainNow
			currWeather.wind = windNow
			currWeather.snow = snowNow
			currWeather.temperature = realTemperature
			currWeather.temperatureFeel = feelTemperature
				
			#Saving the object we just got with the new information so that our database has updated information about aurora weather 
			currWeather.save()
		
		finalWeatherInfoList = list()
		for singleTie in userToWeatherTieList:
			currWeather = weather.objects.get(cityCode = singleTie.cityCode.cityCode)
			finalWeatherInfoList.append(currWeather)
			

		#I could theoretically return more information but for now I will not 
		context = {
			'finalWeatherInfoList':finalWeatherInfoList,
		}
		return render(request,'weatherHome/index.html',context=context)
	
	else:
		#basically Everything I have here is what should be shown if you are not logged in 
		#City code for Aurora 
		auroraCityCode= '4883817'
		if weather.objects.filter(cityCode=auroraCityCode).exists():
			#I am getting the current weather associated with this city code
			currWeather = weather.objects.get(cityCode = auroraCityCode)
			apiLink = "https://api.openweathermap.org/data/2.5/weather?id={}&appid=e11569a6d5c1f254fa71baae792905e1"
			if currWeather.within_fifteen_min():
				#here we should return the data in the database because the data is still close enough to up to date 
				context = {
					'temperature':currWeather.temperature,
					'location':currWeather.dateOfWeather,
				}
				return render(request,'weatherHome/index.html',context=context)
			else :
				#calling a function that returns a dictionary with relevent information about weather
				weatherInfo = weatherCityInfo ( auroraCityCode, apiLink)
				
				#filling some variables with information about the current weather from the weatherInfo dictionary 
				realTemperature = weatherInfo['realTemperature']
				feelTemperature = weatherInfo['feelTemperature']
				snowNow = weatherInfo['snowNow']
				rainNow = weatherInfo['rainNow']
				windNow = weatherInfo['windNow']
				now = weatherInfo['timeNow']
				
				#I got the currweather object above when I got the city with a certain id
				#now I am giving it updated data
				currWeather.dateOfWeather = now
				currWeather.rain = rainNow
				currWeather.wind = windNow
				currWeather.snow = snowNow
				currWeather.temperature = realTemperature
				currWeather.temperatureFeel = feelTemperature
				
				#Saving the object we just got with the new information so that our database has updated information about aurora weather 
				currWeather.save()
				
				#I could theoretically return more information but for now I will not 
				context = {
					'temperature':currWeather.temperature,
					'location':currWeather.dateOfWeather,
				}
				return render(request,'weatherHome/index.html',context=context)
		else:
			print('hello there is a big mistake if you see this because aurora should be in there by default ')
            return render(request,'weatherHome/index.html')
			#there is no way that aurora is not in the database considering I manually put it in so we don't need anything in the else 
			#if I know that aurora is in there do I even need this if else?!?!?
			#I don't think so 
	
def about(request):
	return render(request,'weatherHome/about.html')
	
