from django.contrib import admin

# Register your models here.
#relative import so we are using .models to say from this directory go to models and grab weather model
from .models import weather

admin.site.register(weather)