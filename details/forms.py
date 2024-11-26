from django.forms import *
from .models import *
from django import forms
from django_select2.forms import Select2Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from dal import autocomplete


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'service']

class UserCustomerForm(UserCreationForm):
    title = forms.ModelChoiceField(queryset=Title.objects.all(), required=False)
    patient_name = forms.CharField(max_length=50)
    mobile = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=False)
    age = forms.CharField(max_length=4, required=False)
    patient_address = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username','email']  # Default User fields

    def save(self, commit=True):
        user = super(UserCustomerForm, self).save(commit=False)
        if commit:
            user.save()
        
        # Create a corresponding Customer object with user as a foreign key
        customer = Customer.objects.create(
            user=user,
            title=self.cleaned_data.get('title'),
            patient_name=self.cleaned_data.get('patient_name'),
            mobile=self.cleaned_data.get('mobile'),
            email=self.cleaned_data.get('email'),
            gender=self.cleaned_data.get('gender'),
            age=self.cleaned_data.get('age'),
            patient_address=self.cleaned_data.get('patient_address')
        )
        customer_group, created = Group.objects.get_or_create(name='Customer')
        user.groups.add(customer_group)
        return user

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
        

class VisitForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=autocomplete.ModelSelect2(url='customer-autocomplete')  # This URL will point to your autocomplete view
    )
    class Meta:
        model = HomeVisit
        fields = ['customer','visit_date', 'location', 'status']
        # widgets = {
        #     'customer': autocomplete.ModelSelect2(url='customer-autocomplete'),
        #     # 'doctor': autocomplete.ModelSelect2(url='doctor-autocomplete'),
        # }


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
    collected_by = forms.ModelChoiceField(
            queryset=Tech.objects.all(),
            required = False,
            empty_label="Select collected_by",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    
    tested_by = forms.ModelChoiceField(
            queryset=Tech.objects.all(),
            required = False,
            empty_label="Select tested_by",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    report_by = forms.ModelChoiceField(
            queryset=Tech.objects.all(),
            required = False,
            empty_label="Select report_by",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
        )
    collected_datetime = forms.DateTimeField(
            required = False,)
    tested_datetime = forms.DateTimeField(
            required = False,)
    report_datetime = forms.DateTimeField(
            required = False,)
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['collected_at', 'referred_by','collected_date','expected_complete_date','tests','customer','order_id']
        # 'collected_datetime','tested_datetime','report_datetime','collected_by','report_by','tested_by']
        
        widgets = {
            'collected_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M',),
            'tested_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'report_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(FillValuesForm, self).__init__(*args, **kwargs)
        self.fields['collected_datetime'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['tested_datetime'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['report_datetime'].input_formats = ('%Y-%m-%dT%H:%M',)

class HomeVisitForm(ModelForm):
    visit_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',   # Add CSS class for styling
                'placeholder': 'collected date',  # Set the placeholder
                'type': 'date',           # This is important for the calendar to show
            }
        ),
        label="Visited Date",  # Optional: Add a label for the form field
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        empty_label="Select Customer",
        widget=Select2Widget(attrs={'class': 'form-control'}),  # Use Select2Widget for searchable dropdown
    )
    
    visitor = forms.ModelChoiceField(
            queryset=Tech.objects.all(),
            empty_label="Select Visitor",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
    )
    status = forms.ModelChoiceField(
            queryset=VisitStatus.objects.all(),
            empty_label="Select Status",  # Adds the placeholder option
            widget=forms.Select(attrs={
                'class': 'form-control'
            })
    )
    location = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's Location"})
    )
    googlemaps_link = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter patient's Location googlemaps_link"})
    )
    notes = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': "Enter notes"})
    )
    class Meta:
        model = HomeVisit
        fields = "__all__"
