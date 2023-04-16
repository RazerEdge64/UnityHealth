
from django.contrib import admin
from django.urls import path

from app.views import dashboard
from app.views.doctors import doctors
from app.views.patients import patients
from app.views.appointments import appointments
from app.views.requests import ajax


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dashboard.home, name="home"),
    path('home/', dashboard.home, name="home"),

    path('login/', dashboard.login, name="login"),

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

    # Requests
    path('get_appointments_ajax/', ajax.get_appointments_ajax, name="get_appointments"),
    path('get_doctors_ajax/', ajax.get_doctors_ajax, name="get_doctors"),
    path('get_patients_ajax/', ajax.get_patients_ajax, name="get_patients"),
    

]
