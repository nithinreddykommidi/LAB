from django.forms import *
from .models import Customer, Test, Doctor,Date, Order

class CusromerForm(ModelForm):
        class Meta:
            model = Customer
            fields = ['patient_name', 'mobile', 'email', 'gender', 'age']
            widgets = {'gender': Select(),
                       }
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer','collected_at','referred_by','collected_date','expected_complete_date','tests','collection_status']
        widgets = {'customer': Select(),
                   'collected_at': Select(),
                   'referred_by': Select(),
                   'collected_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),
                   'expected_complete_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),
                   'tests': CheckboxSelectMultiple(),
                   'collection_status': CheckboxSelectMultiple(),
                   }

class GroupingForm(ModelForm):
        class Meta:
            model = Order
            fields = ['group', 'rh']


class CBPForm(ModelForm):
    class Meta:
        model = Order
        fields = ['WBC', 'RBC', 'platelets']

class EyeForm(ModelForm):
    class Meta:
        model = Order
        fields = ['left_eye', 'right_eye']

class UrineForm(ModelForm):
    class Meta:
        model = Order
        fields = ['bilrubine']
    
class MyForm(ModelForm):
        class Meta:
            model = Date
            fields = ['required_date']
            widgets = {'required_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),}

