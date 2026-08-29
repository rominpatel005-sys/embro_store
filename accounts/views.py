from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.signing import Signer, BadSignature
from django.core.mail import send_mail
from django.urls import reverse
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

signer = Signer()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You are now logged in.")
            login(request, user)
            
            # Send verification email
            try:
                token = signer.sign(user.id)
                verify_url = request.build_absolute_uri(
                    reverse('accounts:verify_email_confirm', kwargs={'token': token})
                )
                subject = "Verify your Embro Store Email"
                message = f"Hi {user.first_name},\n\nPlease verify your email by clicking this link:\n{verify_url}\n\nRegards,\nEmbro Store Team"
                send_mail(subject, message, 'support@embrostore.com', [user.email])
                messages.info(request, "A verification email has been sent to you.")
            except Exception as e:
                # Fallback if email sending fails (e.g. backend error)
                print(f"Error sending verification email: {e}")
                
            return redirect('products:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', 'products:home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('products:home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def verify_email_request(request):
    user = request.user
    if user.profile.email_verified:
        messages.info(request, "Your email is already verified.")
        return redirect('accounts:profile')
    try:
        token = signer.sign(user.id)
        verify_url = request.build_absolute_uri(
            reverse('accounts:verify_email_confirm', kwargs={'token': token})
        )
        subject = "Verify your Embro Store Email"
        message = f"Hi {user.first_name},\n\nPlease verify your email by clicking this link:\n{verify_url}\n\nRegards,\nEmbro Store Team"
        send_mail(subject, message, 'support@embrostore.com', [user.email])
        messages.success(request, "Verification email has been sent.")
    except Exception as e:
        messages.error(request, f"Could not send email: {e}")
    return redirect('accounts:profile')

def verify_email_confirm(request, token):
    try:
        user_id = signer.unsign(token)
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        user.profile.email_verified = True
        user.profile.save()
        messages.success(request, "Email verified successfully!")
        if request.user.is_authenticated and request.user.id == user.id:
            return redirect('accounts:profile')
        return redirect('accounts:login')
    except (BadSignature, User.DoesNotExist):
        messages.error(request, "The verification link is invalid or expired.")
        return redirect('products:home')
