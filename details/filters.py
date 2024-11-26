import django_filters
from .models import Customer, HomeVisit, Order, Tech
from .autocomplete import *

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['patient_name']

class CustomerFilter(django_filters.FilterSet):
    patient_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['patient_name', 'email', 'mobile']


class VisitFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(queryset=Customer.objects.all())
    visitor = django_filters.ModelChoiceFilter(queryset=Tech.objects.all())   
    visit_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'form-control',  # Optionally, add form-control class for Bootstrap styling
                'type': 'date'  # Use 'date' input type to display a date picker
            }
        )
    )
    class Meta:
        model = HomeVisit
        fields = ['customer', 'visitor', 'visit_date', 'location','status']


class OrderFilter(django_filters.FilterSet):
    collected_date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'form-control',  # Optionally, add form-control class for Bootstrap styling
                'type': 'date'  # Use 'date' input type to display a date picker
            }
        )
    )
    class Meta:
        model = Order
        fields = ['collected_date','customer']
