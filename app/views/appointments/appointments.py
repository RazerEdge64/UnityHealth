from .. import helper

from django.shortcuts import render

TEMPLATE_DIR = "appointments/"


def appointments(request):

    # Get Patients
    patient_names = helper.get_patients()
    # Get Doctors
    doctor_names = helper.get_doctors()

    return render(request, TEMPLATE_DIR+'appointments.html', {'PATIENTS': patient_names, 'DOCTORS': doctor_names})

def appointment_confirmation(request):
    return render(request, TEMPLATE_DIR+'appointment_confirmation.html')