from django.contrib import admin
from .models import Test,Doctor,Patient

# Register your models here.

admin.site.register(Test)
admin.site.register(Doctor)
admin.site.register(Patient)
