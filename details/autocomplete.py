from dal import autocomplete
from .models import Customer, Doctor

class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Customer.objects.none()
        qs = Customer.objects.all()
        if self.q:
            qs = qs.filter(patient_name__icontains=self.q)
        return qs


class TechAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tech.objects.none()
        qs = Tech.objects.all()
        if self.q:  # This is the query string the user typed
            qs = qs.filter(name__icontains=self.q)  # Assuming Tech has a 'name' field

        return qs
