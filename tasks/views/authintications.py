from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.forms import RegistrationForm, LoginForm
from django.views import View
from tasks.models import CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class RegistrationView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 
                    'Email already exists. Please choose a different one.'
                )
            else:
                form.save()
                messages.success(request,
                    f'Account created for {email}. You can now log in.'
                )
                return redirect('login')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, f'Welcome, {email}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password. Please try again.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Wrong Username or password')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
