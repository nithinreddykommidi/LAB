from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Patient, Test, Doctor
from .forms import PatientForm, GroupingForm, UrineForm, CBPForm,EyeForm,MyForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

def get_pat_id(request):
    s = request.META.get('HTTP_REFERER')
    s = (s.split('/'))
    s = s = [x for x in s if x.isdigit()][0]
    patient = Patient.objects.get(id=s)
    return patient
@login_required(login_url='user_login')
def home(request):
    tests = Test.get_all_tests()
    form = PatientForm()
    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'Home.html', {'tests': tests, 'form': form})
@login_required(login_url='user_login')
def patients_list(request):
    patients = Patient.get_all_patients()
    return render(request, 'patients.html', {'patients': patients})

@login_required(login_url='user_login')
def doctors_list(request):
    doctors = Doctor.get_all_doctors()
    return render(request, 'Doctors.html', {'doctors': doctors})

@login_required(login_url='user_login')
def details(request,pk):
    patient = Patient.objects.get(id=pk)
    tests = patient.tests.all()
    return render(request,'Details.html',{'patient': patient, 'tests': tests})

@login_required(login_url='user_login')
def fill_values(request,pk):
    patient = Patient.objects.get(id=pk)
    patient_tests = patient.tests.all()
    context = {'patient':patient, 'patient_tests':patient_tests}
    return render(request,'fill_values.html',context)



@login_required(login_url='user_login')
def delete_user(request,pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()
    return  redirect('patients_list')

@login_required(login_url='user_login')
def doctor(request,pk):
    doc = Doctor.objects.get(id=pk)
    patients = doc.patient_set.all()

    return render(request,'doctor_details.html',{'patients':patients})

@login_required(login_url='user_login')
def CBP(request):
    patient = get_pat_id(request)
    form = CBPForm(instance=patient)
    if request.method == 'POST':
        form = CBPForm(request.POST,instance=patient)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/CBP.html',{'form':form,'patient':patient})

@login_required(login_url='user_login')
def group(request):
    patient = get_pat_id(request)
    form = GroupingForm(instance=patient)
    if request.method == 'POST':
        form = GroupingForm(request.POST,instance=patient)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/group.html',{'form':form,'patient':patient})

@login_required(login_url='user_login')
def urine(request):
    patient = get_pat_id(request)
    form = UrineForm(instance=patient)
    if request.method == 'POST':
        form = UrineForm(request.POST,instance=patient)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/Urine.html',{'form':form,'patient':patient})

@login_required(login_url='user_login')
def eye(request):
    patient = get_pat_id(request)
    form = EyeForm(instance=patient)
    if request.method == 'POST':
        form = EyeForm(request.POST,instance=patient)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'TESTS/Eye.html',{'form':form,'patient':patient})

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
def print_CBP(request):
    patient = get_pat_id(request)
    return render(request, 'TESTS/print_CBP.html',{'patient':patient})


@login_required(login_url='user_login')
def print_group(request):
    patient = get_pat_id(request)
    return render(request, 'TESTS/print_group.html',{'patient':patient})


@login_required(login_url='user_login')
def print_urine(request):
    patient = get_pat_id(request)
    return render(request, 'TESTS/print_urine.html',{'patient':patient})


@login_required(login_url='user_login')
def print_eye(request):
    patient = get_pat_id(request)
    return render(request, 'TESTS/print_Eye.html',{'patient':patient})

def urine_pdf(request):
    patient = get_pat_id(request)
    template_path = '/home/nithinreddykommidi424/LAB_CSS/details/Templates/TESTS/urinepdf.html'
    context = {'patient': patient}
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

def CBP_pdf(request):
    patient = get_pat_id(request)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/CBPpdf.html'
    context = {'patient': patient}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def Eye_pdf(request):
    patient = get_pat_id(request)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/Eyepdf.html'
    context = {'patient': patient}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def group_pdf(request):
    patient = get_pat_id(request)
    template_path = 'E:/LAB_CSS/details/Templates/TESTS/grouppdf.html'
    context = {'patient': patient}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# def pending_samples(request):
#     patients = Patient.get_all_patients()
#     p = []
#     for patient in patients:
#         patient_tests = patient.tests.all()
#         pen = patient.collection_status.all()
#         for i in patient_tests:
#             if i not in pen:
#                 p.append(patient)
#     p = set(p)
#     pending_tests = {}
#     for i in p:
#         pt = []
#         patient_tests = i.tests.all()
#         pen = i.collection_status.all()
#         for test in patient_tests:
#             if test not in pen:
#                 pt.append(test)
#         pending_tests[i] = pt
#
#
#
#     print(pending_tests)

def pending_samples(request):
        patients = Patient.get_all_patients()
        pending_tests = {}
        for patient in patients:
            # Get tests that are not in the collection_status of the patient
            pending_patient_tests = patient.tests.exclude(id__in=patient.collection_status.all())
            if pending_patient_tests.exists():
                pending_tests[patient] = list(pending_patient_tests)

        # print(pending_tests)
        return render(request,'pending.html',{'pending_tests':pending_tests})


def my_view(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['required_date']
            patients_with_collected_date = Patient.objects.filter(collected_date=datetime.date(selected_date.year, selected_date.month, selected_date.day))
        todays_total = 0
        todays_docs = {}
        for pats in patients_with_collected_date:
            todays_total += pats.get_total()
            doc = pats.referred_by
            comm = pats.commision_to_doc
            if doc in todays_docs:
                todays_docs[doc] = todays_docs[doc] + comm
            else:
               todays_docs[doc] = comm
    else:
        form = MyForm()
        patients_with_collected_date = None
        todays_total =  None
        todays_docs = None
    return render(request, 'daily_totals.html', {'form': form, 'patients_with_collected_date': patients_with_collected_date , 'todays_total': todays_total, 'todays_docs':todays_docs})
    