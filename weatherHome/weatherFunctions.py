from datetime import datetime
from weatherHome.models import countryAndCode
from django.conf.urls.static import static
import json
import requests

#Function Name: kalvinToFahrenheit
#Function that converts kalvin to fahrenheit
def kalvinToFahrenheit(kalvin):
	fahrenheit = kalvin *1.8 - 459.67
	return fahrenheit

#Function Name : fahrenheitToCelsius
#function that converts fahrenheit to celsius
def fahrenheitToCelsius(fahrenheit):
	celsius = (fahrenheit -32) * 5/9
	return celsius
	
#Function Name: weatherCityInfo
#Parameters: 
	#cityCode -> string that identifies the city with an id. 
	#apiLink -> string that has link for the api we will use has a bracket so we can put in the city code when we want to 
#Returns a dictionary that holds all weather information that I want to get from the json file 
#In a nutshell it goes to the openWeather api for a city code and gets the weather data that I want and puts it into a dictionary that we return
#that way I don't have to do any of that json mumbojumbo, rather I can call this funciton and get a dictionary with all the information I could want
#I also deal with properly getting the data here like converting from f->k and checking if it is snowing or raining that way I don't have to do that in og funciton call
def weatherCityInfo(cityCode,apiLink):
	#we have a dictionary to store our stuff in 
	#I wonder if I could have used a more efficient data structure than a dictionary
	weatherInfo = dict()
	
	#getting the information that the link has
	#formatting the string so I use the city code that I want to 
	response = requests.get(apiLink.format(cityCode))
	#loading it into a dictionary for me to access I think
	weatherInfoJson = json.loads(response.text)	
	
	#adding information to the dictionary that we want 
	weatherInfo.update( {'realTemperature': kalvinToFahrenheit(weatherInfoJson['main']['temp']) })
	weatherInfo.update({'feelTemperature': kalvinToFahrenheit(weatherInfoJson['main']['feels_like'])})
	weatherInfo.update({'snowNow': 0})
	weatherInfo.update({'windNow': weatherInfoJson['wind']['speed']})
	weatherInfo.update({'rainNow': 0})
	# datetime object containing current date and time
	#https://docs.python.org/3/library/datetime.html
	#Right above is where I can find more information about this data type among others dealing with date time. I will probably look this up at other points
	weatherInfo.update({'timeNow': datetime.now()})
	
	#checking if it is raining
	if "rain" in weatherInfoJson.keys():
		#rain volume for the last one hour in mm
		weatherInfo.update({'rainNow': weatherInfoJson['rain']['1h']})
	#Checking if it is snowing
	if "snow" in weatherInfoJson.keys():
		#snow volume for last one hour in mm 
		weatherInfo.update({'snowNow': weatherInfoJson['snow']['1h']})
	
	return weatherInfo
	
#Function Name: getCityCode
#gets the city code from the information we pass it
def getCityCode(cityName, countryName, zipcode):
	#Opening local json file that has the cityCode and other information about the city code
	print('trying to open the local json file')
	with open("static/json/city.list.json", encoding='utf-8') as read_file:
		data = json.load(read_file)
		
	#if the city the person put is only there once with the country code
	#then I don't need to get any more info because there is only one place it could because
	listOfCities = list()
	#getting what the country code is for this country name 
	countryAndCodeObj = countryAndCode.objects.get(countryName = countryName)
	twoCharCountryCode = countryAndCodeObj.twoCharCountryCode
	
	for location in data:
		if(location['name'] == cityName and location['country'] == twoCharCountryCode):
			listOfCities.append(location)
			
	#if more than one city has that name and is in that country we enter here
	if len(listOfCities) > 1:
		#api link but we will enter the zipcode and twoCharcountrycode 
		apiLink = 'http://api.openweathermap.org/data/2.5/weather?zip={zip},{twoChar}&appid=e11569a6d5c1f254fa71baae792905e1'
		response = requests.get(apiLink.format(zip = zipcode, twoChar = twoCharCountryCode.lower())).text
		apiInfo = json.loads(response)

		#no here I should be getting latt and long from actual json file
		lattJsonAPI = apiInfo['coord']['lat']
		longJsonAPI = apiInfo['coord']['lon']
		#We are now entering a loop to find out which single city is the one we want
		for city in listOfCities:
			#latt and long for city list data
			lattJsonLocal = city['coord']['lat']
			longJsonLocal = city['coord']['lon']
			
			#getting a bound for the latt and long from the api weather
			lattMore = lattJsonAPI + .5
			lattLess = lattJsonAPI - .5
			longMore = longJsonAPI + .5
			longLess = longJsonAPI - .5
			
			#checking which of the cities is within an acceptable bound to be accepted as the city the user wanted from their data.
			if lattMore > lattJsonLocal and lattLess < lattJsonLocal:
				if longMore > longJsonLocal and longLess < longJsonLocal:
					return city['id']
					
	else: 
		#only one city with that name and in that country
		singleCity = listOfCities[0]
		return singleCity['id']