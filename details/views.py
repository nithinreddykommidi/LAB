from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import Customer, Test, Doctor, Order, Title, UNITSANDRANGES
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
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
from .filters import CustomerFilter, VisitFilter, OrderFilter
from .utils import send_order_notification

# Helper function to check if user belongs to one of the specified groups
def group_required(group_names):
    if not isinstance(group_names, (list, tuple)):
        group_names = [group_names]  # Ensure it's always a list or tuple
    
    def in_groups(user):
        return user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=group_names).exists())
    
    return user_passes_test(in_groups)
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
@group_required(['Techician'])
def register_customer(request):
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
            # Assign the user to the "Customer" group (if you have it set up)
            customer_group, created = Group.objects.get_or_create(name='Customer')
            user.groups.add(customer_group)
            subject = 'Welcome'
            message = f"please use https://gg.com to with username:{customer.patient_name} and password: Maheshnit@5"
            send_order_notification(to_email=customer.email, subject=subject, message=message)
            return redirect('/')
    return render(request, 'New Customer.html', {'form': form})

@login_required(login_url='user_login')
@group_required(['Techician'])
def create_visit(request):
    form = HomeVisitForm()
    if request.method == 'POST':
        form = HomeVisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'New Visit.html', {'form': form})

@login_required(login_url='user_login')
@group_required(['Techician'])
def edit_visit(request,pk):
    instance = HomeVisit.objects.get(id=pk)
    form = HomeVisitForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('visits_list'))
    return render(request,'New Visit.html',{'form':form})

@login_required(login_url='user_login')
@group_required(['Techician'])
def home(request):
    tests = Test.get_all_tests()
    form = NewOrderForm()
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            field1_value = cleaned_data['customer']
            subject = 'New Order Created'
            message = f"An order has been successfully created."
            send_order_notification(to_email=field1_value.email, subject=subject, message=message)
            return redirect(reverse('orders_list'))
    return render(request, 'Home.html', {'tests': tests, 'form': form})

@login_required(login_url='user_login')
@group_required(['Techician'])
def orders_list(request):
    f = OrderFilter(request.GET, queryset=Order.objects.all())
    return render(request, 'orders.html', {'filter': f})
    # list_of_orders = Order.objects.all()
    # p = Paginator(Order.objects.all(), 11)
    # page = request.GET.get('page')
    # orders = p.get_page(page)
    # nums = "a" * orders.paginator.num_pages
    # return render(request, 'orders.html', 
	# 	{'list_of_orders': list_of_orders,'orders': orders,'nums':nums})

@login_required(login_url='user_login')
@group_required(['Techician'])
def doctors_list(request):
    doctors = Doctor.get_all_doctors()
    return render(request, 'Doctors.html', {'doctors': doctors})

@login_required(login_url='user_login')
@group_required(['Techician'])
def visits_list(request):
    f = VisitFilter(request.GET, queryset=HomeVisit.objects.all())
    return render(request, 'visits_list.html', {'filter': f})

@login_required(login_url='user_login')
@group_required(['Techician'])
def customer_details(request,pk):
    patient = Customer.objects.get(id=pk)
    orders = patient.order_set.all()
    return render(request,'Customer Details.html',{'patient': patient, 'orders':orders})

@login_required(login_url='user_login')
@group_required(['Techician'])
def order_details(request,order_id):
    order = Order.objects.get(order_id=order_id)
    tests = order.tests.all()
    return render(request,'Order Details.html',{'order': order, 'tests': tests})

@login_required(login_url='user_login')
@group_required(['Techician'])
def edit_order(request,order_id):
    instance = Order.objects.get(order_id=order_id)
    form = NewOrderForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('order_details', kwargs={'order_id': order_id}))
    order = Order.objects.get(order_id=order_id)
    return render(request,'edit_order.html',{'order': order, 'form':form})

@login_required(login_url='user_login')
@group_required(['Techician'])
def delete_order(request,pk):
    order = Order.objects.get(order_id=pk)
    order.delete()
    return  redirect('orders_list')

@login_required(login_url='user_login')
@group_required(['Techician'])
def delete_visit(request,pk):
    visit = HomeVisit.objects.get(id=pk)
    visit.delete()
    return  redirect('visits_list')

@login_required(login_url='user_login')
@group_required(['Techician'])
def delete_customer(request,pk):
    patient = Customer.objects.get(id=pk)
    patient.delete()
    return  redirect('patients_list')

@login_required(login_url='user_login')
@group_required(['Techician'])
def doctor(request,pk):
    doctor = Doctor.objects.get(id=pk)
    orders = doctor.order_set.all()
    return render(request,'doctor_details.html',{'doctor':doctor, 'orders':orders})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the logged-in user is in the 'Customer' group
            if user.groups.filter(name='Customer').exists():
                return redirect('customer_portal')  # Redirect customer to their dashboard
            elif user.groups.filter(name='Doctor').exists():
                return redirect('doctor_portal')
            else:
                return redirect('home')  # Redirect other users to homepage
        else:
            # Invalid credentials, handle login failure
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def pending_samples(request):
        orders = Order.get_all_orders()
        pending_tests = {}
        for order in orders:
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

@login_required(login_url='user_login')
@group_required(['Techician'])
def patients_list(request):
    f = CustomerFilter(request.GET, queryset=Customer.objects.all())
    return render(request, 'patients.html', {'filter': f})

@login_required(login_url='user_login')
@group_required(['Techician'])
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
@group_required(['Techician'])
def fill_values(request, uuid):
    order = get_object_or_404(Order, order_id=uuid)
    form = FillValuesForm(instance = order)
    units = get_object_or_404(UNITSANDRANGES, id=1)
    if not order.customer:
        return HttpResponse("Order does not have an associated customer", status=400)
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

@login_required(login_url='user_login')
@group_required(['Customer'])
def customer_portal(request):
    usr = (str(request.user))
    customer = Customer.objects.get(patient_name=usr)
    orders = customer.order_set.all()  
    visits = customer.homevisit_set.all()  
    return render(request, 'portal.html', {
        'customer': customer,
        'visits': visits,
        'orders': orders
    })
@login_required(login_url='user_login')
@group_required(['Customer'])
def download_report(request, report_id):
    report = get_object_or_404(TestReport, id=report_id, customer__user=request.user)
    response = HttpResponse(report.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={report.filename}'
    return response

@login_required(login_url='user_login')
@group_required(['Doctor'])
def doctor_portal(request):
    usr = (str(request.user))
    doctor = Doctor.objects.get(doctor_name=usr)
    orders = doctor.order_set.all()
    # visits = customer.homevisit_set.all()  
    return render(request, 'docportal.html', {
        'doctor': doctor,
        # 'visits': visits,
        'orders': orders
    })