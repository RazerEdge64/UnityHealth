
from django.contrib import admin
from django.urls import path

from app.views import dashboard
from app.views import login
from app.views.doctors import doctors
from app.views.doctors import doctor_operations
from app.views.patients import patients
from app.views.appointments import appointments
from app.views.patients import user_operations
from app.views.requests import ajax


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dashboard.login, name="login"),
    path('home/', dashboard.home, name="home"),

    path('login/', dashboard.login, name="login"),

    path('check_login/', login.check_login, name="login"),
    path('logout/', login.user_logout, name="user_logout"),

    path('doctors/', doctors.doctors, name="show_doctors"),
    path('create_new_doctor/', doctors.create_new_doctor, name="create_new_doctor"),
    path('delete_doctor/', doctors.delete_doctor, name="delete_doctor"),
    path('edit_doctor/', doctors.edit_doctor, name="edit_doctor"),

    path('patients/', patients.patients, name="show_patients"),
    path('create_new_patient/', patients.create_new_patient, name="create_new_patient"),
    path('delete_patient/', patients.delete_patient, name="delete_patient"),
    path('delete_patients/', patients.delete_patients, name="delete_patients"),
    path('edit_patient/', patients.edit_patient, name="edit_patient"),

    path('appointments/', appointments.appointments, name="show_appointments"),
    path('appointment_confirmation/', appointments.appointment_confirmation, name="appointment_confirmation"),

    path('user', user_operations.user_dashboard, name="user_dashboard"),
    path('select_time/', user_operations.select_time, name="select_time"),

    path('doctor_appointments/', doctor_operations.doctor_appointments, name="doctor_appointments"),
    path('show_time_slots/', doctor_operations.show_time_slots, name="show_time_slots"),
    path('create_time_slots/', doctor_operations.create_time_slots, name="create_time_slots"),

    # Requests
    path('get_appointments_ajax/', ajax.get_appointments_ajax, name="get_appointments"),
    path('get_doctors_ajax/', ajax.get_doctors_ajax, name="get_doctors"),
    path('get_patients_ajax/', ajax.get_patients_ajax, name="get_patients"),
    path('fetch_hospitals/', ajax.fetch_hospitals, name="fetch_hospitals"),
    path('fetch_doctors/', ajax.fetch_doctors, name="fetch_doctors"),
    path('get_time_slots/', ajax.get_time_slots, name="get_time_slots"),
    path('delete_time_slot/', ajax.delete_time_slot, name="delete_time_slot"),
    path('get_time_slots_for_patients/', ajax.get_time_slots_for_patients, name="get_time_slots_for_patients"),
    

]
