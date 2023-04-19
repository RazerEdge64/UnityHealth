from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...database.connections import cursor, cnx

TEMPLATE_DIR = "patients/"

@login_required
def user_dashboard(request):
    # render a datatable with the existing appointments.

    # return render(request, TEMPLATE_DIR+'select_doctor.html')
    return render(request, TEMPLATE_DIR+'current_appointments.html')

def select_doctor(request):
    return render(request, TEMPLATE_DIR+'select_doctor.html')


def select_time(request):
    doctor_id = request.GET.get('doctor_id')

    return render(request, TEMPLATE_DIR+'book_appointment.html')


