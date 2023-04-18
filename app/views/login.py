from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def check_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return redirect('/login')
    if user.is_superuser:
        login(request, user)
        return redirect('home')
    elif user.get_username() == "patient":
        login(request, user)
        # change this to patient screens
        return redirect('/user')
    else:
        login(request, user)
        # change this to doctor screens
        return redirect('/doctor_appointments')

def user_logout(request):
    logout(request)
    return redirect('/login')

