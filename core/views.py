from django.shortcuts import render, redirect
from django.contrib.auth.models import  User,auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

@login_required(login_url='sign_in')
def index(request):
    try:
        in_user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        in_user_profile = None
    return render(request, 'index.html', {'user_profile': in_user_profile})


def sign_up(request):
    if request.method == 'POST':
        in_username = request.POST['username']
        in_email = request.POST['email']
        in_password = request.POST['password']
        in_password2 = request.POST['password2']
        if in_password == in_password2:
            if User.objects.filter(email=in_email).exists():
                messages.info(request, 'Email Taken')
                return redirect('sign_up')
            elif User.objects.filter(username=in_username):
                messages.info(request, 'Username Taken')
            else:
                new_user = User.objects.create_user(username=in_username, email=in_email, password=in_password)
                new_user.save()
                logged_user = auth.authenticate(username=in_username, password=in_password)
                auth.login(request, logged_user)
                return redirect('setting')

            user_model = User.objects.get(username=in_username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('sign_in')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('sign_up')

    return render(request, 'signup.html')


def sign_in(request):
    if request.method == 'POST':
        in_username = request.POST['username']
        in_password = request.POST['password']
        user = auth.authenticate(username=in_username, password=in_password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            redirect('sign_in')

    return render(request, 'signin.html')


@login_required(login_url='sign_in')
def log_out(request):
    auth.logout(request)
    return redirect('sign_in')


@login_required(login_url='sign_in')
def setting(request):
    try:
        in_user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        in_user_profile = None

    if in_user_profile is not None:
        if request.method == 'POST':
            in_bio = request.POST['bio']
            in_location = request.POST['location']
            in_image = None

            if request.FILES.get('image') is None:
                in_image = in_user_profile.profile_img
            if request.FILES.get('image') is not None:
                in_image = request.FILES.get('image')

            in_user_profile.profile_img = in_image
            in_user_profile.bio = in_bio
            in_user_profile.location = in_location
            in_user_profile.save()
            return redirect('setting')

    return render(request, 'setting.html', {'user_profile': in_user_profile})
