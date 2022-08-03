from django.contrib import admin
from .models import Profile, Edge, Pairing

# Register your models here.
admin.site.register(Profile)
admin.site.register(Edge)
admin.site.register(Pairing)