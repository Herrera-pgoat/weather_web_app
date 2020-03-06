from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from weatherHome.models import countryAndCode,  weather, weatherForUsers
from weatherHome.weatherFunctions import getCityCode , weatherCityInfo
from datetime import datetime
import requests 
from django.http import HttpResponse

# Function Name:addLocation 
def addLocation(request):
	if request.method == "POST":
		#Getting all the data from the form they submitted 
		userCountry = request.POST['country']
		userState  = request.POST['stateName']
		userCity  = request.POST['cityName']
		userZipcode = request.POST['zipcode']
		#Getting the name of the user who is requesting weather of this location 
		user = request.user
		
		#getting the city code
		cityCode = getCityCode(userCity,userCountry,userZipcode)
			
		#I we already have a city with that city code 
		if weather.objects.filter(cityCode = cityCode).exists():
			weatherInstance = weather.objects.get(cityCode = cityCode)
			#go to the model of users and city codes and save this city code to the user city stuff 
			userWeatherTie = weatherForUsers.objects.create(username = user, cityCode = weatherInstance)
			userWeatherTie.save()
		#We enter here if the information they gave us did not lead to a single city in the world according to the json file and parsing api info
		elif cityCode == 'badData':
			messages.error(request, 'We could not find a city with that information. Please verify what you entered is correct!')
			#The thing in the redirect is what it is called in the views 
			return redirect('addLoc')
		else:
			#that place doesn't even exist so we will make it exist
			#apiLink with the citycode rather than the zipcode
			apiLink = "https://api.openweathermap.org/data/2.5/weather?id={}&appid=e11569a6d5c1f254fa71baae792905e1"
					
			#calling a function that returns a dictionary with relevent information about weather
			weatherInfo = weatherCityInfo ( cityCode, apiLink)
				
			#filling some variables with information about the current weather from the weatherInfo dictionary 
			realTemperature = weatherInfo['realTemperature']
			feelTemperature = weatherInfo['feelTemperature']
			snowNow = weatherInfo['snowNow']
			rainNow = weatherInfo['rainNow']
			windNow = weatherInfo['windNow']
			now = weatherInfo['timeNow']	

			weatherInstance = weather.objects.create( dateOfWeather = now, temperature = realTemperature, temperatureFeel = feelTemperature, wind = windNow, 
			rain = rainNow, snow = snowNow, cityCode = cityCode,zipcode = userZipcode ,cityName = userCity  , stateName = userState   ,countryName =userCountry  )
			weatherInstance.save()
			
			#saving this tie between the user and the weather city they want info from 
			userWeatherTie = weatherForUsers.objects.create(username = user, cityCode = weatherInstance)
			userWeatherTie.save()
		
		#Now I get information of city stuff based on the info they gave me and get the city code 
		#call function that returns the city code when we give it the info we have from form 
		cityAddedInformation = userCity + userState + userCountry + userZipcode 
		messages.success(request,cityAddedInformation)
		
	#getting all of the country names and codes
	countries = countryAndCode.objects.all()
	
	context = {
		'countries': countries
	}
	return render(request,'settingsPages/addLocation.html',context)
	
# Function Name: remove Location
def removeLocation(request):
#what I need to do here is if I get a post message I look for certain information in a form 
#then I delete that value in the database depending on that selected value

	#We enter this if statement when we chose to delete a city 
	if request.method == 'POST':
		#Getting the cityCode of the city they want to remove and the user data stuff
		removingCity = request.POST['City']
		currentUser = request.user
		
		
		#Now I just need to call the database to remove that item and we are out
		cityList = weatherForUsers.objects.filter(username=currentUser )
		
		for city in cityList:
			if city.cityCode.cityCode == removingCity:
				cityDeletingMessage = "You have successfully deleted " + str(city.cityCode)
				messages.success(request,cityDeletingMessage)
				city.cityCode.delete()
				break
		#cityDeleting.delete()
		#cityDeletingMessage = "You have successfully deleted a city :)"
		#messages.success(request,cityDeletingMessage)

	#Getting all of the cities that the user is tied with 
	userCities = weatherForUsers.objects.filter(username = request.user)

	context = {
		'userCities': userCities
	}
	
	return render(request,'settingsPages/removeLocation.html',context)
