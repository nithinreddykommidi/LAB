from django.contrib import admin
from .models import Test,Doctor,Customer,Order

# Register your models here.

admin.site.register(Test)
admin.site.register(Order)
admin.site.register(Doctor)
admin.site.register(Customer)
