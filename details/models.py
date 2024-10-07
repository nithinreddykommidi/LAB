from django.db import models
from datetime import datetime
from django.db.models import Max
import uuid


class Test(models.Model):
    is_collected = {('yes', 'yes'),
              ('no', 'no')}
    test_id = models.AutoField(primary_key=True)
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

class Title(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Customer(models.Model):
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING,null=True)
    patient_name = models.CharField(max_length=50)
    mobile = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING,null=True)
    age = models.CharField(max_length=4, null=True)
    patient_address = models.CharField(max_length=150)
    # willing_to_get_SMS = models.BooleanField(default=True)

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
class Tech(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class VisitStatus(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_name = models.CharField(max_length=50)
    commission = models.IntegerField()
    doctor_mobile = models.IntegerField(null=True)
    doctor_email = models.EmailField(null=True)

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
    
    def get_selected_tests(self):
        return self.tests.all()
        
    @property
    def commision_to_doc(self):
        doc_commission = self.referred_by.commission
        bill = self.get_total()
        try:
            return int(float(doc_commission) / 100 * float(bill))
        except ZeroDivisionError:
            return 0
    @staticmethod
    def get_all_orders():
        return Order.objects.all()

    def __str__(self):
        return self.customer.patient_name
        # return str(self.order_id)

    collected_at = models.ForeignKey(Locations, on_delete=models.DO_NOTHING,null=True)
    referred_by = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING,null=True)
    collected_date = models.DateField(null= True)
    expected_complete_date = models.DateField(null=True)
    tests = models.ManyToManyField(Test, blank=False)
    customer = models.ForeignKey(Customer,on_delete=models.DO_NOTHING, blank=False)
    # collection_status = models.ManyToManyField(Test, blank=True,null = True,related_name='stat')
    # created_at = models.DateTimeField(datetime.now(),null=True)
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    collected_by = models.ForeignKey(Tech, on_delete=models.DO_NOTHING,null=True, related_name='collected_by', blank = True)
    tested_by = models.ForeignKey(Tech, on_delete=models.DO_NOTHING,null=True, related_name='tested_by', blank = True)
    report_by = models.ForeignKey(Tech, on_delete=models.DO_NOTHING,null=True, related_name='report_by',blank=True)
    collected_datetime = models.DateTimeField(null=True)  # For date and time
    tested_datetime = models.DateTimeField(null=True)  # For date and time
    report_datetime = models.DateTimeField(null=True)  # For date and time



# Fields for tests
# GLYCOSYLATED HEMOGLOBIN (HBA1c)
    hba1c = models.CharField(max_length=10, blank= True)
# BLOOD UREA NITROGEN - BUN
    blood_urea_nitrogen = models.CharField(max_length=10, blank=True)
# COTININE
    cotinine = models.CharField(max_length=10, blank=True)
# ERYTHROCYTE SEDIMENTATION RATE( ESR)
    esr_1_hour = models.CharField(max_length=10, blank=True)
# HBsAg - Hepatitis B surface Antigen
    hbsag = models.CharField(max_length=10, blank=True)
# HIV I & II Elisa
    hiv_1_and_2 = models.CharField(max_length=10, blank=True)
# COMPLETE URINE EXAMINATION
    colour = models.CharField(max_length=10, blank=True)

    specific_gravity = models.CharField(max_length=10, blank=True)

    ph = models.CharField(max_length=10, blank=True)

    blood = models.CharField(max_length=10, blank=True)

    albumin = models.CharField(max_length=10, blank=True)

    sugar = models.CharField(max_length=10, blank=True)

    ketone_bodies = models.CharField(max_length=10, blank=True)

    nitrite = models.CharField(max_length=10, blank=True)

    urobilinogen = models.CharField(max_length=10, blank=True)

    leucocytes = models.CharField(max_length=10, blank=True)

    bile_salts = models.CharField(max_length=10, blank=True)

    bile_pigments = models.CharField(max_length=10, blank=True)

    pus_cells = models.CharField(max_length=10, blank=True)

    epithelial_cells = models.CharField(max_length=10, blank=True)

    rbcs = models.CharField(max_length=10, blank=True)

    bacteria = models.CharField(max_length=10, blank=True)

    others = models.CharField(max_length=10, blank=True)
# HAEMOGRAM
    haemoglobin = models.CharField(max_length=10, blank=True)

    rbc_count = models.CharField(max_length=10, blank=True)

    pcv = models.CharField(max_length=10, blank=True)

    platelets = models.CharField(max_length=10, blank=True)

    wbc = models.CharField(max_length=10, blank=True)

    neutrophils = models.CharField(max_length=10, blank=True)

    lymphocytes = models.CharField(max_length=10, blank=True)

    eosinophils = models.CharField(max_length=10, blank=True)

    monocytes = models.CharField(max_length=10, blank=True)

    basophils = models.CharField(max_length=10, blank=True)

    mcv = models.CharField(max_length=10, blank=True)

    mchc = models.CharField(max_length=10, blank=True)

    mch = models.CharField(max_length=10, blank=True)
# RANDOM BLOOD SUGAR
    random_blood_sugar = models.CharField(max_length=10, blank=True)
# RFT/KFT
    uric_acid = models.CharField(max_length=10, blank=True)

    serum_creatinine = models.CharField(max_length=10, blank=True)
# LIPID PROFILE
    total_cholesterol = models.CharField(max_length=10, blank=True)

    hdl = models.CharField(max_length=10, blank=True)

    ldl = models.CharField(max_length=10, blank=True)

    vldl = models.CharField(max_length=10, blank=True)

    triglycerides = models.CharField(max_length=10, blank=True)

    chol_hdl_ratio = models.CharField(max_length=10, blank=True)
# LIVER FUNCTION TEST
    total_bilirubin = models.CharField(max_length=10, blank=True)

    direct_bilirubin = models.CharField(max_length=10, blank=True)

    indirect_bilirubin = models.CharField(max_length=10, blank=True)

    alkaline_phosphatase = models.CharField(max_length=10, blank=True)

    serum_gpt = models.CharField(max_length=10, blank=True)

    serum_got = models.CharField(max_length=10, blank=True)

    total_proteins = models.CharField(max_length=10, blank=True)

    albumin = models.CharField(max_length=10, blank=True)

    globulin = models.CharField(max_length=10, blank=True)

    alb_glob_ratio = models.CharField(max_length=10, blank=True)

    ggtp = models.CharField(max_length=10, blank=True)

class UNITSANDRANGES(models.Model):
# UNITSANDRANGES for tests
# GLYCOSYLATED HEMOGLOBIN (HBA1c)
    hba1c_unit = models.CharField(max_length=10, blank= True)
    hba1c_reference_range = models.TextField(blank= True)
# BLOOD UREA NITROGEN - BUN
    blood_urea_nitrogen_unit = models.CharField(max_length=10, blank=True)
    blood_urea_nitrogen_reference_range = models.CharField(max_length=250, blank=True)
# COTININE
    cotinine_unit = models.CharField(max_length=10, blank=True)
    cotinine_reference_range = models.CharField(max_length=250, blank=True)
# ERYTHROCYTE SEDIMENTATION RATE( ESR)
    esr_1_hour_unit = models.CharField(max_length=10, blank=True)
    esr_1_hour_reference_range = models.CharField(max_length=250, blank=True)
# HBsAg - Hepatitis B surface Antigen
    hbsag_unit = models.CharField(max_length=10, blank=True)
    hbsag_reference_range = models.CharField(max_length=250, blank=True)
# HIV I & II Elisa
    hiv_1_and_2_unit = models.CharField(max_length=10, blank=True)
    hiv_1_and_2_reference_range = models.CharField(max_length=250, blank=True)
# COMPLETE URINE EXAMINATION
    colour_unit = models.CharField(max_length=10, blank=True)
    colour_reference_range = models.CharField(max_length=250, blank=True)

    specific_gravity_unit = models.CharField(max_length=10, blank=True)
    specific_gravity_reference_range = models.CharField(max_length=250, blank=True)

    ph_unit = models.CharField(max_length=10, blank=True)
    ph_reference_range = models.CharField(max_length=250, blank=True)

    blood_unit = models.CharField(max_length=10, blank=True)
    blood_reference_range = models.CharField(max_length=250, blank=True)

    albumin_unit = models.CharField(max_length=10, blank=True)
    albumin_reference_range = models.CharField(max_length=250, blank=True)

    sugar_unit = models.CharField(max_length=10, blank=True)
    sugar_reference_range = models.CharField(max_length=250, blank=True)

    ketone_bodies_unit = models.CharField(max_length=10, blank=True)
    ketone_bodies_reference_range = models.CharField(max_length=250, blank=True)

    nitrite_unit = models.CharField(max_length=10, blank=True)
    nitrite_reference_range = models.CharField(max_length=250, blank=True)

    urobilinogen_unit = models.CharField(max_length=10, blank=True)
    urobilinogen_reference_range = models.CharField(max_length=250, blank=True)

    leucocytes_unit = models.CharField(max_length=10, blank=True)
    leucocytes_reference_range = models.CharField(max_length=250, blank=True)

    bile_salts_unit = models.CharField(max_length=10, blank=True)
    bile_salts_reference_range = models.CharField(max_length=250, blank=True)

    bile_pigments_unit = models.CharField(max_length=10, blank=True)
    bile_pigments_reference_range = models.CharField(max_length=250, blank=True)

    pus_cells_unit = models.CharField(max_length=10, blank=True)
    pus_cells_reference_range = models.CharField(max_length=250, blank=True)

    epithelial_cells_unit = models.CharField(max_length=10, blank=True)
    epithelial_cells_reference_range = models.CharField(max_length=250, blank=True)

    rbcs_unit = models.CharField(max_length=10, blank=True)
    rbcs_reference_range = models.CharField(max_length=250, blank=True)

    bacteria_unit = models.CharField(max_length=10, blank=True)
    bacteria_reference_range = models.CharField(max_length=250, blank=True)

    others_unit = models.CharField(max_length=10, blank=True)
    others_reference_range = models.CharField(max_length=250, blank=True)
# HAEMOGRAM
    haemoglobin_unit = models.CharField(max_length=10, blank=True)
    haemoglobin_reference_range = models.CharField(max_length=250, blank=True)

    rbc_count_unit = models.CharField(max_length=10, blank=True)
    rbc_count_reference_range = models.CharField(max_length=250, blank=True)

    pcv_unit = models.CharField(max_length=10, blank=True)
    pcv_reference_range = models.CharField(max_length=250, blank=True)

    platelets_unit = models.CharField(max_length=10, blank=True)
    platelets_reference_range = models.CharField(max_length=250, blank=True)

    wbc_unit = models.CharField(max_length=10, blank=True)
    wbc_reference_range = models.CharField(max_length=250, blank=True)

    neutrophils_unit = models.CharField(max_length=10, blank=True)
    neutrophils_reference_range = models.CharField(max_length=250, blank=True)

    lymphocytes_unit = models.CharField(max_length=10, blank=True)
    lymphocytes_reference_range = models.CharField(max_length=250, blank=True)

    eosinophils_unit = models.CharField(max_length=10, blank=True)
    eosinophils_reference_range = models.CharField(max_length=250, blank=True)

    monocytes_unit = models.CharField(max_length=10, blank=True)
    monocytes_reference_range = models.CharField(max_length=250, blank=True)

    basophils_unit = models.CharField(max_length=10, blank=True)
    basophils_reference_range = models.CharField(max_length=250, blank=True)

    mcv_unit = models.CharField(max_length=10, blank=True)
    mcv_reference_range = models.CharField(max_length=250, blank=True)

    mchc_unit = models.CharField(max_length=10, blank=True)
    mchc_reference_range = models.CharField(max_length=250, blank=True)

    mch_unit = models.CharField(max_length=10, blank=True)
    mch_reference_range = models.CharField(max_length=250, blank=True)
# RANDOM BLOOD SUGAR
    random_blood_sugar_unit = models.CharField(max_length=10, blank=True)
    random_blood_sugar_reference_range = models.CharField(max_length=250, blank=True)
# RFT/KFT
    uric_acid_unit = models.CharField(max_length=10, blank=True)
    uric_acid_reference_range = models.CharField(max_length=250, blank=True)

    serum_creatinine_unit = models.CharField(max_length=10, blank=True)
    serum_creatinine_reference_range = models.CharField(max_length=250, blank=True)
# LIPID PROFILE
    total_cholesterol_unit = models.CharField(max_length=10, blank=True)
    total_cholesterol_reference_range = models.CharField(max_length=250, blank=True)

    hdl_unit = models.CharField(max_length=10, blank=True)
    hdl_reference_range = models.CharField(max_length=250, blank=True)

    ldl_unit = models.CharField(max_length=10, blank=True)
    ldl_reference_range = models.CharField(max_length=250, blank=True)

    vldl_unit = models.CharField(max_length=10, blank=True)
    vldl_reference_range = models.CharField(max_length=250, blank=True)

    triglycerides_unit = models.CharField(max_length=10, blank=True)
    triglycerides_reference_range = models.CharField(max_length=250, blank=True)

    chol_hdl_ratio_unit = models.CharField(max_length=10, blank=True)
    chol_hdl_ratio_reference_range = models.CharField(max_length=250, blank=True)
# LIVER FUNCTION TEST
    total_bilirubin_unit = models.CharField(max_length=10, blank=True)
    total_bilirubin_reference_range = models.CharField(max_length=250, blank=True)

    direct_bilirubin_unit = models.CharField(max_length=10, blank=True)
    direct_bilirubin_reference_range = models.CharField(max_length=250, blank=True)

    indirect_bilirubin_unit = models.CharField(max_length=10, blank=True)
    indirect_bilirubin_reference_range = models.CharField(max_length=250, blank=True)

    alkaline_phosphatase_unit = models.CharField(max_length=10, blank=True)
    alkaline_phosphatase_reference_range = models.CharField(max_length=250, blank=True)

    serum_gpt_unit = models.CharField(max_length=10, blank=True)
    serum_gpt_reference_range = models.CharField(max_length=250, blank=True)

    serum_got_unit = models.CharField(max_length=10, blank=True)
    serum_got_reference_range = models.CharField(max_length=250, blank=True)

    total_proteins_unit = models.CharField(max_length=10, blank=True)
    total_proteins_reference_range = models.CharField(max_length=250, blank=True)

    albumin_unit = models.CharField(max_length=10, blank=True)
    albumin_reference_range = models.CharField(max_length=250, blank=True)

    globulin_unit = models.CharField(max_length=10, blank=True)
    globulin_reference_range = models.CharField(max_length=250, blank=True)

    alb_glob_ratio_unit = models.CharField(max_length=10, blank=True)
    alb_glob_ratio_reference_range = models.CharField(max_length=250, blank=True)

    ggtp_unit = models.CharField(max_length=10, blank=True)
    ggtp_reference_range = models.CharField(max_length=250, blank=True)

class HomeVisit(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length = 50, blank= True)
    googlemaps_link = models.CharField(max_length = 50, blank= True)
    notes = models.CharField(max_length = 50, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Tech, on_delete=models.CASCADE)
    status = models.ForeignKey(VisitStatus, on_delete=models.CASCADE)
