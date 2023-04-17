from django.shortcuts import render
from django.contrib.auth.decorators import login_required

TEMPLATE_DIR = "user/"

@login_required
def user_dashboard(request):
    # Fetch all hospitals and feed.
    return render(request, TEMPLATE_DIR+'select_doctor.html')

def select_time(request):
    return render(request, TEMPLATE_DIR+'book_appointment.html')


