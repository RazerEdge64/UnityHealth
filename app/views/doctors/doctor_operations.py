from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .d_helper import DHelper as helper

TEMPLATE_DIR = "doctors/"

@login_required
def doctor_appointments(request):
    return render(request, TEMPLATE_DIR+"doctor_appointments.html")

def time_slots(request):
    return render(request, TEMPLATE_DIR+"time_slots.html")