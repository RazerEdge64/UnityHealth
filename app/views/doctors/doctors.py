from .. import helper
from django.shortcuts import render, redirect
from .d_helper import DHelper as helper


TEMPLATE_DIR = "admin/doctors/"


def doctors(request):

    # Get Doctors
    doctor_names = helper.get_doctors_master()

    return render(request, TEMPLATE_DIR+'doctors.html', {'DOCTORS': doctor_names})


def create_new_doctor(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    gender = request.POST.get("gender")
    phone_no = request.POST.get("phone_no")
    date_of_birth = request.POST.get("date_of_birth")
    office_fax_no = request.POST.get("office_fax_no")
    experience = request.POST.get("experience")

    new_doctor = {}
    new_doctor['first_name'] = first_name
    new_doctor['last_name'] = last_name
    new_doctor['gender'] = gender
    new_doctor['phone_no'] = phone_no
    new_doctor['office_fax_no'] = office_fax_no
    # fix the way in which date gets stored.
    new_doctor['date_of_birth'] = date_of_birth
    new_doctor['experience'] = experience
    helper.add_doctor(new_doctor)

    return redirect('/doctors')

def delete_doctor(request):
    doctor_id = request.POST.get("delete_id")
    helper.delete_doctor(doctor_id)
    return redirect('/doctors')

def edit_doctor(request):
    doctor_id = request.POST.get("edit_doctor_id")
    first_name = request.POST.get("edit_doctor_first_name")
    last_name = request.POST.get("edit_doctor_last_name")
    gender = request.POST.get("edit_doctor_gender")
    phone_no = request.POST.get("edit_doctor_ph_no")
    date_of_birth = request.POST.get("edit_doctor_dob")
    experience = request.POST.get("edit_doctor_experience")
    office_fax_no = request.POST.get("edit_doctor_office_fax_no")

    updated_doctor = {}
    updated_doctor['doctor_id'] = doctor_id
    updated_doctor['first_name'] = first_name
    updated_doctor['last_name'] = last_name
    updated_doctor['gender'] = gender
    updated_doctor['phone_no'] = phone_no
    updated_doctor['date_of_birth'] = date_of_birth
    updated_doctor['experience'] = experience
    updated_doctor['office_fax_no'] = office_fax_no

    helper.edit_doctor(updated_doctor)
    return redirect('/doctors')