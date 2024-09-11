from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Customer, Test, Doctor, Order, Title
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
import re
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import CustomerFilter
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from weasyprint import HTML
import os


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
            form.save()
            return redirect('/')
    return render(request, 'New Customer.html', {'tests': tests, 'form': form})
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
    p = Paginator(Order.objects.all(), 2)
    page = request.GET.get('page')
    orders = p.get_page(page)
    nums = "a" * orders.paginator.num_pages
    return render(request, 'orders.html', 
		{'list_of_orders': list_of_orders,
		'orders': orders,
		'nums':nums}
		)
@login_required(login_url='user_login')
def doctors_list(request):
    doctors = Doctor.get_all_doctors()
    return render(request, 'Doctors.html', {'doctors': doctors})

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
    # tests = order.tests.all()
    print(print(request.POST))
    return render(request,'edit_order.html',{'order': order, 'form':form})

@login_required(login_url='user_login')
def fill_values(request,pk):
    patient = Order.objects.get(order_id=pk)
    patient_tests = patient.tests.all()
    context = {'patient':patient, 'patient_tests':patient_tests}
    return render(request,'fill_values.html',context)



@login_required(login_url='user_login')
def delete_order(request,pk):
    order = Order.objects.get(order_id=pk)
    order.delete()
    return  redirect('orders_list')

@login_required(login_url='user_login')
def doctor(request,pk):
    doctor = Doctor.objects.get(id=pk)
    orders = doctor.order_set.all()
    return render(request,'doctor_details.html',{'doctor':doctor, 'orders':orders})

@login_required(login_url='user_login')
def CBP(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    form = CBPForm(instance=Orderid)
    if request.method == 'POST':
        form = CBPForm(request.POST,instance=Orderid)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/CBP.html',{'form':form,'Orderid':Orderid})

@login_required(login_url='user_login')
def group(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    form = GroupingForm(instance=Orderid)
    if request.method == 'POST':
        form = GroupingForm(request.POST,instance=Orderid)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/group.html',{'form':form,'Orderid':Orderid})

@login_required(login_url='user_login')
def urine(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    form = UrineForm(instance=Orderid)
    if request.method == 'POST':
        form = UrineForm(request.POST,instance=Orderid)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/Urine.html',{'form':form,'Orderid':Orderid})

@login_required(login_url='user_login')
def eye(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    form = EyeForm(instance=Orderid)
    if request.method == 'POST':
        form = EyeForm(request.POST,instance=Orderid)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/Eye.html',{'form':form,'Orderid':Orderid})

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

@login_required(login_url='user_login')
def print_CBP(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    return render(request, 'TESTS/print_CBP.html',{'Orderid':Orderid})


@login_required(login_url='user_login')
def print_group(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    return render(request, 'TESTS/print_group.html',{'Orderid':Orderid})


@login_required(login_url='user_login')
def print_urine(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    return render(request, 'TESTS/print_urine.html',{'Orderid':Orderid})


@login_required(login_url='user_login')
def print_eye(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    return render(request, 'TESTS/print_Eye.html',{'Orderid':Orderid})

def urine_pdf(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    template_path = '/home/nithinreddykommidi424/LAB_CSS/details/Templates/TESTS/urinepdf.html'
    context = {'Orderid': Orderid}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def CBP_pdf(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/CBPpdf.html'
    context = {'Orderid': Orderid}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def Eye_pdf(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/Eyepdf.html'
    context = {'Orderid': Orderid}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def group_pdf(request,uuid):
    Orderid = Order.objects.get(order_id=uuid)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/grouppdf.html'
    context = {'Orderid': Orderid}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


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
    print(customer)

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

def generate_pdf(request, order_id):
    # Get the order details by UUID
    try:
        order = Order.objects.get(order_id=order_id)  # Assuming 'order_id' is the field in the Order model
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Context to pass to the template
    context = {
        'logo_url': 'path/to/your/logo.png',  # Provide your logo URL here
        'barcode': '35443',
        'patient_code': order.customer.id,
        'patient_name': order.customer.patient_name,
        'age': order.customer.age,
        'gender': order.customer.gender.gender,
        'registration_date': order.collected_date,
        'sample_collection_date': order.collected_date,
        'tests': order.tests.all(),
        'subtotal': sum([test.price for test in order.tests.all()]),
        'discount': 200,  # Add logic for calculating discount
        'total': 800,  # Subtotal - Discount
        'paid': 400,  # You can add logic to calculate payments
        'due': 400,  # Add your due calculation here
    }

    # Render HTML content from the template
    html_content = render_to_string('invoice_template.html', context)

    # Create PDF
    pdf_file = HTML(string=html_content).write_pdf()

    # Create a response to serve PDF as a downloadable file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="order_invoice.pdf"'
    return response
