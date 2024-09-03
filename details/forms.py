from django.forms import *
from .models import Patient, Test, Doctor,Date
from django import forms
from bootstrap_datepicker.widgets import DatePicker

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'gender', 'collected_at','referred_by','collected_date','expected_complete_date', 'mobile', 'email','age','tests','collection_status']
        widgets = {'collected_at': Select(),
                   'referred_by': Select(),
                   'collected_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),
                   'expected_complete_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),
                   'tests': CheckboxSelectMultiple(),
                   'collection_status': CheckboxSelectMultiple(),
                   'gender': Select(),}

class GroupingForm(ModelForm):
        class Meta:
            model = Patient
            fields = ['group', 'rh']


class CBPForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['WBC', 'RBC', 'platelets']

class EyeForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['left_eye', 'right_eye']

class UrineForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['bilrubine']
    
class MyForm(ModelForm):
        class Meta:
            model = Date
            fields = ['required_date']
            widgets = {'required_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),}

