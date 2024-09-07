from django.core.exceptions import ObjectDoesNotExist

def get_customer(patient_name, mobile=None):
        # Positive Scenario: When both patient_name and mobile are provided
  if mobile:
    customer = Customer.objects.get(patient_name=patient_name, mobile=mobile)
    print(f"Customer found: {customer.patient_name}, Mobile: {customer.mobile}")
    return customer
  else:
            # Negative Scenario: When only patient_name is provided (mobile is None or not given)
    customer = Customer.objects.get(patient_name=patient_name)
    print(f"Customer found: {customer.patient_name}, Mobile: {customer.mobile}")
    return customer
  
  
customer_1 = get_customer(patient_name='John Doe', mobile=1234567890)

# Negative case: Only patient_name matches, mobile not provided
customer_2 = get_customer(patient_name='Jane Doe')
