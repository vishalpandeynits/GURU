from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm

def signup(request):
	message = None
	if request.method == 'POST':
		form = SignUpForm(request.POST or None)
		if form.is_valid():
			form.save()
			return redirect('/accounts/login')
	else:
		form = SignUpForm()
	return render(request, 'registation/signup.html', {'form': form})

def profiles(request, username):
	p_user = get_object_or_404(User, username=username)
	profile = get_object_or_404(Profile, user=p_user)
	context ={'profile' : profile,}
	return render (request, 'users/profile.html', context)

@login_required
def edit_profile(request,username=None):
	profile = Profile.objects.get(user=request.user)
	print(profile)
	if request.method == "POST":
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if p_form.is_valid():
			p_form.save()
			return redirect(f'/profile/{username}/')
			context ={'profile' : profile}
			return render (request, 'users/profile.html', context)
	else:
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {		
		'p_form' : p_form,
		'profile' : profile,
	}
	return render(request, 'users/edit_profile.html', context)