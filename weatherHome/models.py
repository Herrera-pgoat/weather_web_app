from django.db import models
from datetime import datetime

# Create your models here.
#The class below is called weather but we really want it to be weather  
class weather(models.Model):
	degree = models.DecimalField(max_digits = 3, decimal_places = 1)
	location = models.CharField(max_length = 200)
	date = models.DateTimeField(default=datetime.now)
	climate = models.CharField(max_length = 100)
	fahrenheit = models.BooleanField(default = True)
	def __str__(self):
		return self.date
