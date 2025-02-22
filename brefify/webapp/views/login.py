from django.shortcuts import render
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password, make_password
from  webapp.models import UserProfile
from django.views import View
from django import template

from django.shortcuts import render, redirect
from django.views import View
from webapp.models import UserProfile

from django.contrib.auth import get_user_model

User = get_user_model()
class Login(View):
    def get(self, request):
        if request.session.get('user_id'):
            return redirect('dashboard')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email').strip().lower()  # Normalize email
        password = request.POST.get('password')
        
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                
                # Debugging check
                print(f"Session after login: {dict(request.session)}")
                
                next_url = request.GET.get('dashboard') or 'dashboard'
                return redirect(next_url)
                
            return render(request, 'login.html', {'error': 'Invalid password'})
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email not registered'})

def logout(request):
    request.session.clear()
    return redirect('index')
