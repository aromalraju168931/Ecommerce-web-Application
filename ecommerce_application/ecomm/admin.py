from django.contrib import admin
from .models import Products
from .models import Profile

# Register your models here.
admin.site.register(Products)
admin.site.register(Profile)
