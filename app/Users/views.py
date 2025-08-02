# app/Users/views.py

import os
import logging
from django import forms
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError
import hashlib
import base64
from app.Bookings.models import Booking, Hotel 

logger = logging.getLogger(__name__)

User = get_user_model()

class UserForm(forms.ModelForm):
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
            'required': True,
        }),
        label="Confirm password"
    )

    class Meta:
        model = User
        # fields = ['email', 'username', 'password', 'repeat_password', 'first_name', 'last_name', 'date_of_birth']
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
            }),
            'username': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
                'placeholder': ' ',
                'required': True,
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Select date',
                'type': 'text',
                'datepicker': 'datepicker',
                'datepicker-autohide': 'datepicker-autohide',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Use set_password to hash the password
        if commit:
            user.save()
        return user

class CustomLoginView(LoginView):
    template_name = 'includes/user/user_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home or any other page if the user is already logged in
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if user.isLogin:
            messages.error(self.request, "This user is already logged in from another session.")
            return self.form_invalid(form)
        user.isLogin = True
        user.save()
        logger.debug(f"User {user.username} logged in successfully.")
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.isLogin = False
            user.save()
            # Log out all sessions of the user
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            for session in sessions:
                data = session.get_decoded()
                if user.id == data.get('_auth_user_id'):
                    session.delete()
        auth_logout(request)
        logger.debug(f"User {user.username} logged out successfully.")
        return redirect(self.next_page)

@csrf_protect
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or any other page if the user is already logged in
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            add_user_to_ldap(user)
            return redirect('user_success')
    else:
        form = UserForm()
    return render(request, 'includes/user/user_register.html', {'form': form})

def user_success(request):
    return render(request, 'includes/user/user_success.html')

@login_required
def user_profile(request):
    return render(request, 'includes/user/user_profile.html', {'user': request.user})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.Bookings.models import Booking, Hotel  # Correct import path for the Booking and Hotel models
from django.core.paginator import Paginator

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'includes/user/user_profile.html', {'user': user})

@login_required
def booking_history(request):
    user = request.user
    bookings = Booking.objects.filter(user_id=user.id).select_related('hotel').order_by('-start_date')

    current_date = timezone.now().date()
    for booking in bookings:
        if booking.end_date < current_date:
            booking.status = 'Expired'
        elif booking.start_date > current_date:
            booking.status = 'Upcoming'
        else:
            booking.status = 'Ongoing'

    paginator = Paginator(bookings, 10)  # Show 10 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'includes/booking/booking_history.html', context)

@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        delete_user_from_ldap(user)
        user.delete()  # Permanently delete the user from the Django database
        auth_logout(request)  # Log out the user
        return redirect('login')  # Redirect to the login page
    return render(request, 'includes/user/delete_user_confirm.html', {'user': user})

def add_user_to_ldap(user):
    # Directly set the LDAP server URI, bind DN, and bind password
    ldap_server_uri = 'ldap://10.10.100.95:389'
    ldap_bind_dn = 'cn=admin,dc=example,dc=com'
    ldap_bind_password = 'ubuntu'

    server = Server(ldap_server_uri, get_info=ALL)
    try:
        conn = Connection(server, ldap_bind_dn, ldap_bind_password, auto_bind=True)
        logger.debug("LDAP connection established.")
        
        dn = f"uid={user.username},ou=users,dc=example,dc=com"
        
        # Hash the password using SSHA
        hashed_password = '{SSHA}' + base64.b64encode(hashlib.sha1(user.password.encode('utf-8')).digest()).decode('utf-8')
        
        logger.debug(f"Adding user to LDAP with DN: {dn}")
        logger.debug(f"User details: cn={user.first_name} {user.last_name}, sn={user.last_name}, uid={user.username}, mail={user.email}")

        conn.add(dn, ['inetOrgPerson', 'posixAccount', 'top'], {
            'cn': user.first_name + ' ' + user.last_name,
            'sn': user.last_name,
            'uid': user.username,
            'mail': user.email,
            'userPassword': hashed_password,
            'loginShell': '/bin/bash',
            'uidNumber': '1001',  # Ensure unique UID and GID numbers
            'gidNumber': '1001',
            'homeDirectory': f'/home/{user.username}'
        })
        conn.unbind()
        logger.debug("User added to LDAP.")
    except LDAPSocketOpenError as e:
        logger.error(f"LDAP connection error: {e}")
    except LDAPBindError as e:
        logger.error(f"LDAP bind error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def delete_user_from_ldap(user):
    server = Server('ldap://10.10.100.95:389', get_info=ALL)
    try:
        conn = Connection(server, 'cn=admin,dc=example,dc=com', 'ubuntu', auto_bind=True)
        dn = f"uid={user.username},ou=users,dc=example,dc=com"
        conn.delete(dn)
        conn.unbind()
    except LDAPSocketOpenError as e:
        logger.error(f"LDAP connection error: {e}")
    except LDAPBindError as e:
        logger.error(f"LDAP bind error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")