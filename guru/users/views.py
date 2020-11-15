from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .token import account_activation_token
from .forms import SignUpForm, ProfileUpdateForm
from .models import Profile
from django.contrib import messages
from basic.models import Classroom

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('emails/acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            print( form.cleaned_data.get('email'))
            h=send_mail(mail_subject, message,'vishalpandeynits@gmail.com',[to_email],fail_silently=False,html_message=message)
            print(h)
            messages.add_message(request,messages.SUCCESS,'An Activation link is sent to your \
                    registrated email id.Please visit your email and activate your account.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'signupform': form})


def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request,messages.SUCCESS,'Thank you for your email confirmation. We request you to kindly update your \
            contact details so other users can contact you in case of any need.')
        if user is not None:
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect(f'/profile/{user.username}')
    else:
        messages.add_message(request,messages.WARNING,'Activation link is invalid.')
        return redirect('home')

def profiles(request, username):
    p_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=p_user)
    p_form = my_classes=None
    if p_user == request.user:
        if request.method == "POST":
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            print(request.FILES)
            if p_form.is_valid():
                k=p_form.save(commit=False)
                k.profile_pic=request.FILES['file']
                k.save()
                return redirect(f'/profile/{username}/')
        else:
            instance = request.user.profile
            instance.bio = instance.bio
            p_form = ProfileUpdateForm(instance=request.user.profile)
    if request.user.is_authenticated:
        my_classes = Classroom.objects.all().filter(members=request.user)
    context = {		
        'p_form' : p_form,
        'profile' : profile,
        'classes':my_classes
    }
    return render (request, 'users/profile.html', context)