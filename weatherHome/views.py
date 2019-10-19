from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request,'weatherHome/index.html')
	
def about(request):
	return render(request,'weatherHome/about.html')
