from django.shortcuts import render
from django.contrib.auth.decorators import login_required


TEMPLATE_DIR = "dashboard/"

@login_required
def home(request):

    return render(request, TEMPLATE_DIR+'home.html')


def login(request):
    return render(request, 'login.html')
