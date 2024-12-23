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
from django.urls import path,re_path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home,name = 'home'),
    path('register_customer',register_customer,name='register_customer'),
    path('logout',user_logout,name='user_logout'),
    path('login',user_login, name='user_login'),
    path('patients_list',patients_list, name='patients_list'),
    path('orders_list',orders_list, name='orders_list'),
    path('visits_list',visits_list, name='visits_list'),
    path('create_visit',create_visit, name='create_visit'),
    path('daily_totals',daily_totals, name='daily_totals'),
    path('doctors_list',doctors_list, name='doctors_list'),
    path('pending_samples',home, name='pending_samples'),
    path('<int:pk>/customer_details', customer_details, name='customer_details'),
    path('<order_id>/order_details', order_details, name='order_details'),
    path('<order_id>/edit_order', edit_order, name='edit_order'),
    path('<pk>/edit_visit', edit_visit, name='edit_visit'),
    path('<pk>/delete_order', delete_order, name='delete_order'),
    path('<pk>/delete_visit', delete_visit, name='delete_visit'),
    path('<pk>/delete_customer', delete_customer, name='delete_customer'),
    path('<pk>/doctor', doctor, name='doctor'),
    path('create_order/<int:customer_id>/', create_order_for_customer, name='create_order_for_customer'),
    path('<uuid:order_id>/order_details/invoice/', generate_invoice, name='generate_invoice'),
    path('<uuid:order_id>/generate_pdf_for_tests/', generate_pdf_for_tests, name='generate_pdf_for_tests'),
    path('<pk>/edit_customer_details/', edit_customer, name='edit_customer'),
    path('<uuid:uuid>/fill_values', fill_values, name='fill_values'),
    path('share_report/<uuid:order_id>/', share_report, name='share_report'),
    path('update-range/', update_range, name='update_range'),
    path('select2/', include('django_select2.urls')),
    path('customer-portal/', customer_portal, name='customer_portal'),
    path('doctor-portal/', doctor_portal, name='doctor_portal'),
    path('download-report/<int:report_id>/', download_report, name='download_report'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
