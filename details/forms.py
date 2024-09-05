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
        fields = ['customer', 'collected_at', 'referred_by', 'collected_date', 'expected_complete_date', 'tests', 'collection_status']
        widgets = {
            'customer': Select(attrs={'class': 'form-control custom-select'}),
            'collected_at': Select(attrs={'class': 'form-control custom-select'}),
            'referred_by': Select(attrs={'class': 'form-control custom-select'}),
            'collected_date': DateInput(format='%m/%d/%Y', 
                                        attrs={'class': 'form-control datepicker input-box', 'placeholder': 'MM/DD/YYYY', 'type':'date'}),
            'expected_complete_date': DateInput(format='%m/%d/%Y', 
                                                attrs={'class': 'form-control datepicker input-box', 'placeholder': 'Expected completion date'}),
            'tests': CheckboxSelectMultiple(attrs={'class': 'form-check-inline custom-checkbox-grid'}),
            'collection_status': CheckboxSelectMultiple(attrs={'class': 'form-check-inline switch'}),
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

