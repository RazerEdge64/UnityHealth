from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from ..database.connections import cursor
from ..logs import logger


def check_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return redirect('/login')
    if user.is_superuser:
        login(request, user)
        return redirect('home')
    elif user.groups.filter(name="patients").exists():
        login(request, user)
        
        patient_id = check_user_id(user.first_name, user.last_name)
        return redirect('/user?id='+str(patient_id))
    else:
        login(request, user)
        # change this to doctor screens
        doctor_id = check_doctor_id(user.first_name, user.last_name)
        return redirect('/doctor_appointments?id='+str(doctor_id))


def user_logout(request):
    logout(request)
    return redirect('/login')

def check_user_id(first_name, last_name):
    query = "SELECT patient_id FROM patients WHERE first_name=%s AND last_name=%s"
    cursor.execute(query, (first_name, last_name))
    rows = cursor.fetchall()
    if rows:
        return rows[0][0]
    else:
        return None

def check_doctor_id(first_name, last_name):
    query = "SELECT doctor_id FROM doctors WHERE first_name=%s AND last_name=%s"
    cursor.execute(query, (first_name, last_name))
    rows = cursor.fetchall()
    if rows:
        return rows[0][0]
    else:
        return None
