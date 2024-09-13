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
from .views import *
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
    path('<int:pk>/customer_details', customer_details, name='customer_details'),
    path('<order_id>/order_details', order_details, name='order_details'),
    path('<order_id>/edit_order', edit_order, name='edit_order'),
    path('<pk>/fill_values', fill_values, name='fill_values'),
    path('<pk>/delete_order', delete_order, name='delete_order'),
    path('<pk>/doctor', doctor, name='doctor'),
    path('<uuid:uuid>/Eye', eye, name='Eye'),
    path('<uuid:uuid>/CBP',CBP,name='CBP'),
    path('<uuid:uuid>/group',group,name='group'),
    path('<uuid:uuid>/Urine',urine,name='Urine'),
    path('<uuid:uuid>/Eye',eye,name='Eye'),
    path('<order_id>/print/CBP',print_CBP,name='CBP'),
    path('<order_id>/print/group',print_group,name='group'),
    path('<order_id>/print/Urine',print_urine,name='Urine'),
    # path('pdf/Urine',urine_pdf,name='pdf_Urine'),
    # path('pdf/CBP',urine_pdf,name='pdf_Urine'),
    # path('pdf/Eye',urine_pdf,name='pdf_Urine'),
    # path('pdf/group',urine_pdf,name='pdf_Urine'),
    path('<order_id>/print/Eye',print_eye,name='Eye'),
    path('create_order/<int:customer_id>/', create_order_for_customer, name='create_order_for_customer'),
    path('<uuid:order_id>/order_details/invoice/', generate_pdf, name='generate_pdf'),
    path('<pk>/edit_customer_details/', edit_customer, name='edit_customer'),


]
