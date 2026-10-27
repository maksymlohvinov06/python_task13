from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        middle_name = request.POST.get('middle_name', '')
        role = request.POST.get('role', '2')

        if email and password:
            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    role=int(role)
                )
                return redirect('login')
                
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})

def user_detail(request, user_id):
    try:
        user_obj = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('user_list')
    return render(request, 'authentication/user_detail.html', {'user_obj': user_obj})