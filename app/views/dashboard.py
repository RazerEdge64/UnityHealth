from django.shortcuts import render

TEMPLATE_DIR = "dashboard/"


def home(request):

    return render(request, TEMPLATE_DIR+'home.html')


def login(request):
    return render(request, 'login.html')

