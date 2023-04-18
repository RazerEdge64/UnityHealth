from django.shortcuts import render
from django.contrib.auth.decorators import login_required

TEMPLATE_DIR = "patients/"

@login_required
def user_dashboard(request):
    # Check if user is a doctor
    if request.user.username == "doctor":
        # Render doctor appointments page
        return render(request, "doctors/"+'doctor_appointments.html')
    else:
        # Render select doctor page for other users
        return render(request, TEMPLATE_DIR+'select_doctor.html')


def select_time(request):
    return render(request, TEMPLATE_DIR+'book_appointment.html')


