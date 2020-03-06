from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from weatherHome.models import countryAndCode,  weather, weatherForUsers
from weatherHome.weatherFunctions import getCityCode , weatherCityInfo
from datetime import datetime


# Create your views here.
def createAccount(request):
	#checking if we are in a post
	if request.method == 'POST':
		#Right here I am getting all the information from the form we submitted (POSTED)
		#The thing in the bracket is how it is called in the form's html 
		userFirstName = request.POST['userFirstName']
		userLastName= request.POST['userLastName']
		usernameForm = request.POST['usernameText']
		userEmail = request.POST['userEmail']
		#unsure if I should be hashing now or later ?!?!
		#for now I will hash after I have determined everything is in order. 
		userPassword = request.POST['passwordText']
		passwordConfirm = request.POST['passwordTextConfirm']
		
		#We should go check if the user is unique or not here and if it is not 
		#we tell the user that with an error message. 
		if User.objects.filter(username = usernameForm).exists():
			messages.error(request, 'username already exists pick a new one please ;)')
			return redirect('createAccount')
		
		#We only want an email to be attached to one user 
		if User.objects.filter(email = userEmail).exists():
			messages.error(request, 'that email already exists pick a new one please ;)')
			return redirect('createAccount')
			
		#before I say this form submission is legit I must check if the two passwords are the same
		if userPassword != passwordConfirm :
			messages.error(request, 'The passwords do not match! Put the same one on both texts ')
			return redirect('createAccount')
		#If I am here I know the password is legit			

		#getting an instance of the user database thing 
		newUser = User.objects.create_user(username = usernameForm, password = userPassword, email = userEmail, 
		first_name = userFirstName,last_name = userLastName)
		
		#saving this new user to the database
		newUser.save()
		
#I AM KEEPING THIS BELOW BECAUSE IT IS A RELIC OF WHEN I THOUGHT I COULD MAKE MY USER MODEL WORK MIDWAY THROUGH THE PROJECT 
#IT HAS EMOTIONAL VALUE TO ME AND MY SON (i don't have any children)
#*****************************************************************************************************************************************************		
		#now we actually want to save the user to the User database so we need to get an instance of user then feed it the information. Then save it
		#this the salt where we add it to the password.
	#	userSalt = user.createSalt();
		#we are hashing the password with the function and sending the salt over there
	#	passwordHashedHere = user.encryptString(password,userSalt)
#		now = datetime.now()
#		userInstance = user.objects.create( username = usernameForm, userEmail = email, userFirstName = first_name, userLastName = last_name, 
#		passwordHashed = passwordHashedHere, passwordSalt = userSalt, dateAccountCreated = now)
#		userInstance.save()
#*****************************************************************************************************************************************************
		messages.success(request, 'You are now registered and can log in now')
	
		#right here if passwords match and if the username is unique!
		#right here is where we make the person in the database	
		print('SUBMITTED REG')
		return redirect('createAccount')
	else:
		return render(request,'accounts/createAccount.html')
	
def login(request):
	if request.method == 'POST':
		#getting username and password from the request they put in
		userName = request.POST['usernameText']
		userPassword = request.POST['passwordText']
		
		#checking if there is a valid user with these credentials
		user = auth.authenticate(username=userName, password = userPassword)
		
		#if we got a user with those credentials we enter this if statement
		if user is not None:
			#This will log the user in
			auth.login(request,user)
			messages.success(request,'You are logged in :)')
			return redirect('index')
		else:
			messages.error(request,'No user with that password user combination :(')
			return redirect('login')
	
	else:
		#if the method to here is not a post we just go to login.html like a regular person would. I am a regular person. 
		return render(request,'accounts/login.html')
		
#This is the logout function
def logout(request):
	if request.method == "POST":
		#we want to logout our user and give them a mesage that says they logeed out
		auth.logout(request)
		messages.success(request,'You are now logged out')
		return redirect('index')
	
	