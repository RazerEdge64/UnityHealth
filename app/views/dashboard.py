from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .login import check_doctor_id, check_user_id


TEMPLATE_DIR = "dashboard/"

@login_required
def home(request):

    if request.user.is_superuser:
        return render(request, TEMPLATE_DIR+'home.html')
    elif request.user.groups.filter(name="doctors").exists():
        doctor_id = check_doctor_id(request.user.first_name, request.user.last_name)
        return redirect('/doctor_appointments?id='+str(doctor_id))
    else:
        patient_id = check_user_id(request.user.first_name, request.user.last_name)
        return redirect('/user?id='+str(patient_id))


def login(request):
    return render(request, 'login.html')
