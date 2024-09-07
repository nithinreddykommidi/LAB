from django.forms import *
from .models import Customer, Test, Doctor,Date, Order, Locations, Gender
from django import forms

class CustomerForm(ModelForm):
        patient_name = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's name"})
    )
        mobile = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's phnone No."})
    )
        email = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's mailID"})
    )
        gender = forms.ModelChoiceField(
            queryset=Gender.objects.all(),
            empty_label="Select Gender",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
        age = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'age'})
    )
        class Meta:
            model = Customer
            fields = ['patient_name', 'mobile', 'email', 'gender', 'age']
            widgets = {'gender': Select(),
                       }
class OrderForm(ModelForm):
    collected_at = forms.ModelChoiceField(
            queryset=Locations.objects.all(),
            empty_label="Select Location",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    
    customer = forms.ModelChoiceField(
            queryset=Customer.objects.all(),
            empty_label="Select Customer",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    referred_by = forms.ModelChoiceField(
            queryset=Doctor.objects.all(),
            empty_label="Select the doctor refered",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    collected_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',   # Add CSS class for styling
                'placeholder': 'collected date',  # Set the placeholder
                'type': 'date',           # This is important for the calendar to show
            }
        ),
        label="Collected Date",  # Optional: Add a label for the form field
    )
    expected_complete_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',   # Add CSS class for styling
                'placeholder': 'collected_date',  # Set the placeholder
                'type': 'date',           # This is important for the calendar to show
            }
        ),
        label="Collected Date",  # Optional: Add a label for the form field
    )
    tests = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),  # Change this to your actual queryset
        widget=forms.CheckboxSelectMultiple(),
        help_text="Please select the tests you want to include.",  # Help text serves as a guide
        label="Available Tests"
    )
    collection_status = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),  # Change this to your actual queryset
        widget=forms.CheckboxSelectMultiple(),
        help_text="Please select the tests you want to include.",  # Help text serves as a guide
        label="Available Tests"
    )
    class Meta:
        model = Order
        fields = ['customer', 'collected_at', 'referred_by', 'collected_date', 'expected_complete_date', 'tests', 'collection_status']

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

class CustomerSearchForm(ModelForm):
    # patient_name = forms.CharField(
    #         widget=forms.TextInput(attrs={'placeholder': "Enter patient's name"})
    # )
    # mobile = forms.CharField(
    #         widget=forms.TextInput(attrs={'placeholder': "Enter patient's phnone No."})
    # )
    # class Meta:
    #         model = Date
    #         fields = ['patient_name','mobile']
    #         required = {'patient_name': False}
    class Meta:
        model = Date
        fields = ['patient_name','mobile']
        # widgets = {'required_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),}

