from django.contrib import admin
from .models import Test,Doctor,Customer,Order,Locations,Gender, Title, UNITSANDRANGES, Tech, HomeVisit, VisitStatus, Appointment

# Register your models here.

admin.site.register(Test)
admin.site.register(Order)
admin.site.register(Doctor)
admin.site.register(Customer)
admin.site.register(Locations)
admin.site.register(Gender)
admin.site.register(Title)
admin.site.register(UNITSANDRANGES)
admin.site.register(Tech)
admin.site.register(HomeVisit)
admin.site.register(VisitStatus)
admin.site.register(Appointment)


