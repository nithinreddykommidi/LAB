from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Customer, Test, Doctor, Order, Title, UNITSANDRANGES
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
import datetime
import re
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import CustomerFilter
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from weasyprint import HTML
import os
from PyPDF2 import PdfMerger
from io import BytesIO
from urllib.parse import quote_plus
from django.conf import settings
from django.contrib.auth.hashers import make_password





def get_pat_id(request):
    s = request.META.get('HTTP_REFERER')
    match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', s)
    if match:
        uuid =  match.group(1)
    else:
        uuid =  None
    Orderid = Order.objects.get(order_id=uuid)
    return Orderid

@login_required(login_url='user_login')
def register_customer(request):
    tests = Test.get_all_tests()
    form = CustomerForm()
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Save the Customer instance first
            customer = form.save(commit=False)

            # Create a User instance
            user = User(
                username=customer.patient_name,  # Or another field that uniquely identifies the user
                email=customer.email,
                first_name=customer.patient_name.split()[0],  # Assuming the first name is the first part
                last_name=customer.patient_name.split()[-1],  # Assuming the last name is the last part
            )

            # Set the default password
            user.password = make_password("Maheshnit@5")  # Set your default password
            user.save()

            # Assign the User instance to the Customer
            customer.user = user
            customer.save()
            
            return redirect('/')
    return render(request, 'New Customer.html', {'tests': tests, 'form': form})

@login_required(login_url='user_login')
def create_visit(request):
    form = HomeVisitForm()
    if request.method == 'POST':
        form = HomeVisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'New Visit.html', {'form': form})

@login_required(login_url='user_login')
def edit_visit(request,pk):
    instance = HomeVisit.objects.get(id=pk)
    form = HomeVisitForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('visits_list'))
    return render(request,'New Visit.html',{'form':form})

@login_required(login_url='user_login')
def home(request):
    tests = Test.get_all_tests()
    form = NewOrderForm()
    if request.method == 'POST':
        form = NewOrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'Home.html', {'tests': tests, 'form': form})

@login_required(login_url='user_login')
def orders_list(request):
    list_of_orders = Order.objects.all()
    p = Paginator(Order.objects.all(), 11)
    page = request.GET.get('page')
    orders = p.get_page(page)
    nums = "a" * orders.paginator.num_pages
    return render(request, 'orders.html', 
		{'list_of_orders': list_of_orders,'orders': orders,'nums':nums})

@login_required(login_url='user_login')
def doctors_list(request):
    doctors = Doctor.get_all_doctors()
    return render(request, 'Doctors.html', {'doctors': doctors})

@login_required(login_url='user_login')
def visits_list(request):
    visits = HomeVisit.objects.all()
    return render(request, 'visits_list.html', {'visits': visits})

@login_required(login_url='user_login')
def customer_details(request,pk):
    patient = Customer.objects.get(id=pk)
    orders = patient.order_set.all()
    return render(request,'Customer Details.html',{'patient': patient, 'orders':orders})

@login_required(login_url='user_login')
def order_details(request,order_id):
    order = Order.objects.get(order_id=order_id)
    tests = order.tests.all()
    return render(request,'Order Details.html',{'order': order, 'tests': tests})


@login_required(login_url='user_login')
def edit_order(request,order_id):
    instance = Order.objects.get(order_id=order_id)
    form = NewOrderForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('order_details', kwargs={'order_id': order_id}))
    order = Order.objects.get(order_id=order_id)
    return render(request,'edit_order.html',{'order': order, 'form':form})


@login_required(login_url='user_login')
def delete_order(request,pk):
    order = Order.objects.get(order_id=pk)
    order.delete()
    return  redirect('orders_list')

@login_required(login_url='user_login')
def delete_visit(request,pk):
    visit = HomeVisit.objects.get(id=pk)
    visit.delete()
    return  redirect('visits_list')

@login_required(login_url='user_login')
def delete_customer(request,pk):
    patient = Customer.objects.get(id=pk)
    patient.delete()
    return  redirect('patients_list')

@login_required(login_url='user_login')
def doctor(request,pk):
    doctor = Doctor.objects.get(id=pk)
    orders = doctor.order_set.all()
    return render(request,'doctor_details.html',{'doctor':doctor, 'orders':orders})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect ('/')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')


def pending_samples(request):
        orders = Order.get_all_orders()
        pending_tests = {}
        for order in orders:
            # Get tests that are not in the collection_status of the patient
            pending_patient_tests = order.tests.exclude(id__in=order.collection_status.all())
            if pending_patient_tests.exists():
                pending_tests[order] = list(pending_patient_tests)
        return render(request,'pending.html',{'pending_tests':pending_tests})


def daily_totals(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['required_date']
            orders_with_collected_date = Order.objects.filter(collected_date=datetime.date(selected_date.year, selected_date.month, selected_date.day))
        todays_total = 0
        todays_docs = {}
        for order in orders_with_collected_date:
            todays_total += order.get_total()
            doc = order.referred_by
            comm = order.commision_to_doc
            if doc in todays_docs:
                todays_docs[doc] = todays_docs[doc] + comm
            else:
               todays_docs[doc] = comm
    else:
        form = MyForm()
        orders_with_collected_date = None
        todays_total =  None
        todays_docs = None
    return render(request, 'daily_totals.html', {'form': form, 'orders_with_collected_date': orders_with_collected_date , 'todays_total': todays_total, 'todays_docs':todays_docs})

def create_order_for_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)  # Get the customer by ID

    if request.method == 'POST':
        form = OrderForm(request.POST)# Pass customer to the form
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer  # Set the customer explicitly before saving
            order.save()
            form.save_m2m()  # Save the ManyToMany relationships
            return redirect('home')  # Redirect to a success page
    else:
        form = OrderForm(initial={'customer': customer})  # Initialize the form with customer

    return render(request, 'order_form.html', {'form': form, 'customer': customer})   


# Helper function to get customer by patient_name and optionally mobile
def get_customer(patient_name=None, mobile=None):
    try:
        # Start with an empty query
        query = Q()

        # If patient_name is provided, use icontains to allow partial matching
        if patient_name:
            query &= Q(patient_name__icontains=patient_name)

        # If mobile is provided, use icontains to allow partial matching
        if mobile:
            query &= Q(mobile__icontains=mobile)

        # Query the database with the constructed Q object
        customers = Customer.objects.filter(query)

        # If no customers are found, return an empty list
        if not customers.exists():
            return []

        return customers  # Return the queryset containing multiple customers

    except ObjectDoesNotExist:
        # Handling case where no customer is found
        return []
# View function
def patients_list(request):
    form = CustomerSearchForm(request.POST or None)  # Handle both POST and GET
    if request.method == 'POST' and form.is_valid():
        patient_name = form.cleaned_data.get('patient_name')
        mobile = form.cleaned_data.get('mobile')
        customers = get_customer(patient_name, mobile)
    else:
        customers = Customer.objects.all()  # By default, list all customers

    return render(request, 'patients.html', {'customers': customers, 'form': form})
    # customers = Customer.get_all_customers()
    # return render(request, 'patients.html', {'customers': customers})

@login_required(login_url='user_login')
def edit_customer(request,pk):
    instance = Customer.objects.get(id=pk)
    form = EditCustomerorm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('customer_details', kwargs={'pk': pk}))
    patient = Customer.objects.get(id=pk)
    orders = patient.order_set.all()
    return render(request,'edit_customer.html',{'patient': patient,'form':form})

def generate_invoice(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)  # Assuming 'order_id' is the field in the Order model
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)
    selected_tests = order.tests.all()
    context = {'order': order, 'selected_tests': selected_tests}  
    html_content = render_to_string('invoice_template.html', context)
    pdf_file = HTML(string=html_content).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="order_invoice.pdf"'
    return response

@login_required(login_url='user_login')
def fill_values(request, uuid):
    # Get the order by order_id
    order = get_object_or_404(Order, order_id=uuid)
    form = FillValuesForm(instance = order)
    units = get_object_or_404(UNITSANDRANGES, id=1)
    if not order.customer:
        return HttpResponse("Order does not have an associated customer", status=400)
    # Get the names of the tests selected for this order
    selected_tests = [test.test_name for test in order.tests.all()]
    if request.method == 'POST':
        form = FillValuesForm(request.POST, instance=order)
        if form.is_valid():
            order.customer = order.customer
            form.save()
            return redirect('order_details', order_id=uuid)
    return render(request, 'fill_values.html', {'form': form, 'order': order, 'selected_tests': selected_tests,'units':units})

def generate_pdf_for_tests(self, order_id):
    try:
        order = Order.objects.get(order_id=order_id)  # Assuming 'order_id' is the field in the Order model
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)    
    units = get_object_or_404(UNITSANDRANGES, id=1)
    selected_tests = [test.test_name for test in order.tests.all()]
    test_pdf_templates = {
        "GLYCOSYLATED HEMOGLOBIN (HBA1c)": "TESTS/HbA1Cpdf.html",
        "BLOOD UREA NITROGEN - BUN ": "TESTS/BUN.html",
        "COMPLETE URINE EXAMINATION": "TESTS/COMPLETE URINE EXAMINATION.html",
        "COTININE": "TESTS/COTININE.html",
        "ERYTHROCYTE SEDIMENTATION RATE( ESR)": "TESTS/ESR.html",
        "HAEMOGRAM": "TESTS/HAEMOGRAM.html",
        "HBsAg - Hepatitis B surface Antigen": "TESTS/HBsAg.html",
        "HIV I & II Elisa": "TESTS/HIV.html",
        "LIPID PROFILE": "TESTS/LIPID PROFILE.html",
        "LIVER FUNCTION TEST": "TESTS/LFT.html",
        "RANDOM BLOOD SUGAR": "TESTS/RANDOM BLOOD SUGAR.html",
        "RFT/KFT": "TESTS/KFT.html",
    }

    # Initialize PDF merger
    pdf_merger = PdfMerger()
    for test in selected_tests:
        template = test_pdf_templates.get(test)  # Get the template path for the test
        if template:
            context = {
                'order': order,
                'test': test,
                'units': units,
            }
            # Generate the PDF using the selected template
            html_content = render_to_string(template, context)
            pdf_file = HTML(string=html_content).write_pdf()

            # Add the PDF file to the merger
            pdf_merger.append(BytesIO(pdf_file))

    # Create a combined PDF output
    merged_pdf = BytesIO()
    pdf_merger.write(merged_pdf)
    pdf_merger.close()

    # Respond with the merged PDF
    response = HttpResponse(merged_pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="merged_test_results.pdf"'
    return response

def generate_pdf_for_test(uuid):
    try:
        order = Order.objects.get(order_id=uuid)  # Assuming 'order_id' is the field in the Order model
    except Order.DoesNotExist:
        return None, None  # Return None if the order is not found
    
    selected_tests = [test.test_name for test in order.tests.all()]
    test_pdf_templates = {
        "GLYCOSYLATED HEMOGLOBIN (HBA1c)": "TESTS/HbA1Cpdf.html",
        "BLOOD UREA NITROGEN - BUN ": "TESTS/BUN.html",
        "COMPLETE URINE EXAMINATION": "TESTS/COMPLETE URINE EXAMINATION.html",
        "COTININE": "TESTS/COTININE.html",
        "ERYTHROCYTE SEDIMENTATION RATE( ESR)": "TESTS/ESR.html",
        "HAEMOGRAM": "TESTS/HAEMOGRAM.html",
        "HBsAg - Hepatitis B surface Antigen": "TESTS/HBsAg.html",
        "HIV I & II Elisa": "TESTS/HIV.html",
        "LIPID PROFILE": "TESTS/LIPID PROFILE.html",
        "LIVER FUNCTION TEST": "TESTS/LFT.html",
        "RANDOM BLOOD SUGAR": "TESTS/RANDOM BLOOD SUGAR.html",
        "RFT/KFT": "TESTS/KFT.html",
    }

    # Initialize PDF merger
    pdf_merger = PdfMerger()
    for test in selected_tests:
        template = test_pdf_templates.get(test)
        if template:
            context = {
                'order': order,
                'test': test,
            }
            # Generate the PDF using the selected template
            html_content = render_to_string(template, context)
            pdf_file = HTML(string=html_content).write_pdf()

            # Add the PDF file to the merger
            pdf_merger.append(BytesIO(pdf_file))

    # Create a combined PDF output
    merged_pdf = BytesIO()
    pdf_merger.write(merged_pdf)
    pdf_merger.close()

    # Define the directory and file name
    pdf_filename = f"order_{uuid}_results.pdf"
    pdf_directory = settings.MEDIA_ROOT

    # Ensure the directory exists
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    pdf_path = os.path.join(pdf_directory, pdf_filename)
    with open(pdf_path, 'wb') as pdf_output:
        pdf_output.write(merged_pdf.getvalue())

    return pdf_filename, pdf_path


def share_report(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)  # Assuming 'order_id' is the field in the Order model
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)    
    
    # Call the generate PDF function to generate the PDF file
    pdf_filename, pdf_path = generate_pdf_for_test(order_id)
    
    if not pdf_filename:
        return HttpResponse("Failed to generate PDF", status=500)

    # Build the download link for the generated PDF file
    download_link = request.build_absolute_uri(f'/media/{pdf_filename}')
    phone = order.customer.mobile
    # share_report_url = reverse('share_report', kwargs={'uuid': str(order.order_id)})


    # Create the WhatsApp pre-filled message with the download link
    message = f"Here is your requested test report: {download_link}"

    # Encode the message for URL compatibility
    whatsapp_message = quote_plus(message)

    # Construct the WhatsApp Web URL
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}&text={whatsapp_message}"

    # Redirect the user to WhatsApp Web with the pre-filled message
    return redirect(whatsapp_url)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
def update_range(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        new_range = request.POST.get('new_range')

        # Get the object you want to update
        obj = get_object_or_404(UNITSANDRANGES, id=1)  # Adjust this to match your logic

        # Update the field dynamically
        if field and hasattr(obj, field):
            setattr(obj, field, new_range)
            obj.save()

            # Return success and the new range value
            return JsonResponse({'status': 'success', 'new_range': new_range})

        # Return failure if something goes wrong
        return JsonResponse({'status': 'fail', 'message': 'Invalid field or data'})
