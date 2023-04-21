from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .login import check_doctor_id, check_user_id
from ..database.connections import cursor, cnx

TEMPLATE_DIR = "dashboard/"


@login_required
def home(request):

    if request.user.is_superuser:
        patients_count, doctors_count, appointments_count, hospitals_count = fetch_details_dashboard()
        return render(request, TEMPLATE_DIR+'home.html', 
            {
                "patients_count" : patients_count,
                "doctors_count" : doctors_count, 
                "appointments_count" : appointments_count,
                "hospitals_count" : hospitals_count
            })
    
    elif request.user.groups.filter(name="doctors").exists():
        doctor_id = check_doctor_id(request.user.first_name, request.user.last_name)
        return redirect('/doctor_appointments?id='+str(doctor_id))
    else:
        patient_id = check_user_id(request.user.first_name, request.user.last_name)
        return redirect('/user?id='+str(patient_id))


def login(request):
    return render(request, 'login.html')



def fetch_details_dashboard():
    query1 = "SELECT COUNT(*) FROM patients"
    query2 = "SELECT COUNT(*) FROM doctors"
    query3 = "SELECT COUNT(*) FROM appointments"
    query4 = "SELECT COUNT(*) FROM hospitals"

    cursor.execute(query1)
    patients_count = cursor.fetchone()[0]
    cursor.execute(query2)
    doctors_count = cursor.fetchone()[0]
    cursor.execute(query3)
    appointments_count = cursor.fetchone()[0]
    cursor.execute(query4)
    hospitals_count = cursor.fetchone()[0]

    return (patients_count, doctors_count, appointments_count, hospitals_count)
