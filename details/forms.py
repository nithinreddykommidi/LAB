from django.forms import *
from .models import *
from django import forms

class CustomerForm(ModelForm):
        title = forms.ModelChoiceField(
            queryset=Title.objects.all(),
            empty_label="Select title",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
    )
        patient_name = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's name"})
    )
        patient_address = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's address"})
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
            fields = ['title','patient_name', 'mobile', 'email', 'gender', 'age', 'patient_address']
            widgets = {'gender': Select(),
                       }
   
class MyForm(ModelForm):
        class Meta:
            model = Date
            fields = ['required_date']
            widgets = {'required_date': DateInput(format='%m/%d/%Y', attrs={'class': 'nithin', 'placeholder': 'Select a date', 'type': 'date'}),}

class CustomerSearchForm(ModelForm):
    class Meta:
        model = Date
        fields = ['patient_name','mobile']

class NewOrderForm(ModelForm):
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
    # collection_status = forms.ModelMultipleChoiceField(
    #     queryset=Test.objects.all(),  # Change this to your actual queryset
    #     widget=forms.CheckboxSelectMultiple(),
    #     help_text="Please select the tests you want to include.",  # Help text serves as a guide
    #     label="Available Tests"
    # )
    class Meta:
        model = Order
        fields = ['customer', 'collected_at', 'referred_by', 'collected_date', 'expected_complete_date', 'tests']

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
    # collection_status = forms.ModelMultipleChoiceField(
    #     queryset=Test.objects.all(),  # Change this to your actual queryset
    #     widget=forms.CheckboxSelectMultiple(),
    #     help_text="Please select the tests you want to include.",  # Help text serves as a guide
    #     label="Available Tests"
    # )
    class Meta:
        model = Order
        fields = ['customer','collected_at', 'referred_by', 'collected_date', 'expected_complete_date', 'tests']

class EditOrderForm(NewOrderForm, ModelForm):
    class Meta:
        model = Order
        fields = ['collected_at', 'referred_by', 'expected_complete_date', 'tests']

class EditCustomerorm(CustomerForm, ModelForm):
    class Meta:
        model = Customer
        fields = ['title','patient_name', 'mobile', 'email', 'gender', 'age', 'patient_address']

class FillValuesForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['collected_at', 'referred_by','collected_date','expected_complete_date','tests','customer','order_id']

    # def __init__(self, *args, **kwargs):
    #     # Pass the selected tests from the view to the form to dynamically show relevant fields
    #     selected_tests = kwargs.pop('selected_tests', [])
    #     super(FillValuesForm, self).__init__(*args, **kwargs)

    #     # Initially hide all fields
    #     all_fields = ['hba1c', 'hba1c_unit', 'blood_urea_nitrogen', 'blood_urea_nitrogen_unit']
    #     for field in all_fields:
    #         self.fields[field].widget = forms.HiddenInput()

    #     # Display the fields related to the selected tests
    #     if 'HbA1C' in selected_tests:
    #         self.fields['hba1c'].widget = forms.TextInput()
    #         self.fields['hba1c_unit'].widget = forms.TextInput()

    #     if 'BLOOD UREA NITROGEN - BUN ' in selected_tests:
    #         self.fields['blood_urea_nitrogen'].widget = forms.TextInput()
    #         self.fields['blood_urea_nitrogen_unit'].widget = forms.TextInput()
