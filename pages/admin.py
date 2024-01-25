from django.contrib import admin
# Register your models here.
from .models import Job, CV

admin.site.register(Job)
admin.site.register(CV)
