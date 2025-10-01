from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    response = redirect('login')

    return response
