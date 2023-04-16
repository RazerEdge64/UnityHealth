from django.shortcuts import redirect, render
from .p_helper import PHelper as helper

TEMPLATE_DIR = "patients/"


def patients(request):
    return render(request, TEMPLATE_DIR+'patients.html')


def create_new_patient(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    gender = request.POST.get("gender")
    phone_no = request.POST.get("phone_no")
    date_of_birth = request.POST.get("date_of_birth")

    new_patient = {}
    new_patient['first_name'] = first_name
    new_patient['last_name'] = last_name
    new_patient['gender'] = gender
    new_patient['phone_no'] = phone_no
    # fix the way in which date gets stored.
    new_patient['date_of_birth'] = date_of_birth
    helper.add_patient(new_patient)

    return redirect('/patients')


def delete_patient(request):
    patient_id = request.POST.get("delete_id")
    helper.delete_patient(patient_id)
    return redirect('/patients')

def delete_patients(request):
    helper.delete_all()
    return redirect('/patients')

def edit_patient(request):
    patient_id = request.POST.get("edit_patient_id")
    first_name = request.POST.get("edit_patient_first_name")
    last_name = request.POST.get("edit_patient_last_name")
    gender = request.POST.get("edit_patient_gender")
    phone_no = request.POST.get("edit_patient_ph_no")
    date_of_birth = request.POST.get("edit_patient_dob")

    updated_patient = {}
    updated_patient['patient_id'] = patient_id
    updated_patient['first_name'] = first_name
    updated_patient['last_name'] = last_name
    updated_patient['gender'] = gender
    updated_patient['phone_no'] = phone_no
    updated_patient['date_of_birth'] = date_of_birth

    helper.edit_patient(updated_patient)
    return redirect('/patients')