from django.db import models
from datetime import datetime
from django.db.models import Max
import uuid


class Test(models.Model):
    is_collected = {('yes', 'yes'),
              ('no', 'no')}
    test_name = models.CharField(max_length=50)
    collection_status = models.CharField(max_length=20, choices=is_collected, blank=False, default='no')
    price = models.IntegerField()

    @staticmethod
    def get_all_tests():
        return Test.objects.all()

    def __str__(self):
        return self.test_name

class Gender(models.Model):
    gender = models.CharField(max_length= 10)

    def __str__(self):
        return self.gender

class Customer(models.Model):
    patient_name = models.CharField(max_length=50)
    mobile = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING,null=True)
    age = models.CharField(max_length=4, null=True)
    @staticmethod
    def get_all_customers():
        return Customer.objects.all()
    def get_last_order_date(self):
        # Fetches the latest collected_date for this customer
        last_order = self.order_set.aggregate(last_order_date=Max('collected_date'))
        return last_order['last_order_date']
    def __str__(self):
        return self.patient_name


    
class Date(models.Model):
    required_date = models.DateField(null= True)
    patient_name = models.CharField(max_length=50,null= True, blank= True)
    mobile = models.IntegerField(null=True, blank= True)



class Locations(models.Model):
        location = models.CharField(max_length=50)

        def __str__(self):
            return self.location


class Doctor(models.Model):
    doctor_name = models.CharField(max_length=50)
    commission = models.IntegerField()
    @staticmethod
    def get_all_doctors():
        return Doctor.objects.all()
    def total_cost(self):
        # doc = Doctor.objects.get(id=pk)
        s = self.order_set.all()
        amount = 0
        for i in s:
            patient_bill = i.get_total()
            amount += patient_bill
        return amount
    def no_of_patients(self):
        # doc = Doctor.objects.get(id=pk)
        s = self.order_set.all()
        return len(s)
    
    def commission_to_doc(self):
        try:
            print((self.commission))
            print(self.total_cost())
            return float(self.commission) / 100 * float(self.total_cost())
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return self.doctor_name


class Order(models.Model):
    def get_total(self):
        # patient_tests = self.tests.all()
        total = sum([test.price for test in self.tests.all()])
        return total
    
    def all_tests(self):
        tests = self.tests.all()
        print(tests.n)
        
    @property
    def commision_to_doc(self):
        doc_commission = self.referred_by.commission
        bill = self.get_total()
        try:
            return int(float(doc_commission) / 100 * float(bill))
        except ZeroDivisionError:
            return 0

    rh_factor = {('+', '+'),
                 ('-', '-')}
    groups = {('A', 'A'),
             ('B', 'B'),
             ('AB', 'AB'),
             ('O', 'O'),
             }

    collected_at = models.ForeignKey(Locations, on_delete=models.DO_NOTHING,null=True)
    referred_by = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING,null=True)
    collected_date = models.DateField(null= True)
    expected_complete_date = models.DateField(null=True)
    tests = models.ManyToManyField(Test, blank=False)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT, blank=False)
    collection_status = models.ManyToManyField(Test, blank=False,related_name='stat')
    created_at = models.DateTimeField(datetime.now(),null=True)
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    # blood grouping
    group = models.CharField(max_length=20, choices=groups, blank=True)
    rh = models.CharField(max_length=20, choices=rh_factor, blank=True)

    # CBP
    WBC = models.CharField(max_length=20, blank=True,default = 'nil')
    RBC = models.CharField(max_length=20, blank=True)
    platelets = models.CharField(max_length=20, blank=True)

    # eye
    left_eye = models.CharField(max_length=20, blank=True)
    right_eye = models.CharField(max_length=20, blank=True)

    # urine
    bilrubine = models.CharField(max_length=20, blank=True)
    @staticmethod
    def get_all_orders():
        return Order.objects.all()

    def __str__(self):
        return self.customer.patient_name
        # return str(self.order_id)







