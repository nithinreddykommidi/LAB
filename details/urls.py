"""LAB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from .views import home,patients_list,doctors_list,customer_details,fill_values,delete_user,doctor,CBP,group,urine,eye,user_login,user_logout,print_CBP,print_eye,print_group,print_urine,urine_pdf,pending_samples,daily_totals,register_customer,orders_list,order_details

urlpatterns = [
    path('', home,name = 'home'),
    path('register_customer',register_customer,name='register_customer'),
    path('logout',user_logout,name='user_logout'),
    path('login',user_login, name='user_login'),
    path('patients_list',patients_list, name='patients_list'),
    path('orders_list',orders_list, name='orders_list'),
    path('daily_totals',daily_totals, name='daily_totals'),
    path('doctors_list',doctors_list, name='doctors_list'),
    path('pending_samples',pending_samples, name='pending_samples'),
    path('<pk>/customer_details', customer_details, name='customer_details'),
    path('<pk>/order_details', order_details, name='order_details'),
    path('<pk>/fill_values', fill_values, name='fill_values'),
    path('<pk>/delete_user', delete_user, name='delete_user'),
    path('<pk>/doctor', doctor, name='doctor'),
    path('<uuid:uuid>/Eye', eye, name='Eye'),
    path('<uuid:uuid>/CBP',CBP,name='CBP'),
    path('<uuid:uuid>/group',group,name='group'),
    path('<uuid:uuid>/Urine',urine,name='Urine'),
    path('<uuid:uuid>/Eye',eye,name='Eye'),
    path('<uuid:uuid>/print/CBP',print_CBP,name='CBP'),
    path('<uuid:uuid>/print/group',print_group,name='group'),
    path('<uuid:uuid>/print/Urine',print_urine,name='Urine'),
    path('pdf/Urine',urine_pdf,name='pdf_Urine'),
    path('pdf/CBP',urine_pdf,name='pdf_Urine'),
    path('pdf/Eye',urine_pdf,name='pdf_Urine'),
    path('pdf/group',urine_pdf,name='pdf_Urine'),
    path('<uuid:uuid>/print/Eye',print_eye,name='Eye'),
]
