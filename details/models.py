from django.db import models
from datetime import datetime
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

class Customer(models.Model):

    choice = {('male', 'male'),
              ('female', 'female')}
        
    patient_name = models.CharField(max_length=50)
    mobile = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=50, choices=choice)
    age = models.CharField(max_length=4, null=True)
    @staticmethod
    def get_all_customers():
        return Customer.objects.all()

    def __str__(self):
        return self.patient_name
    
class Date(models.Model):
        required_date = models.DateField(null= True)


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
        
    locations = {('ATP', 'ATP'),
                 ('KNR', 'KNR')
                 }
    rh_factor = {('+', '+'),
                 ('-', '-')}
    groups = {('A', 'A'),
             ('B', 'B'),
             ('AB', 'AB'),
             ('O', 'O'),
             }

    collected_at = models.CharField(max_length=50, choices=locations)
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







