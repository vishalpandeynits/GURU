from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import *
from .models import *
from datetime import datetime
from django.http import HttpResponse 
def filter_fun(key):
	return key!=""

def home(request):
	if request.method=='POST':
		form = QuestionForm(request.POST or None)
		time= request.POST.get('date')
		time= time.replace("T"," ")
		d = datetime.fromisoformat(time+":00")
		k=d.strftime('%Y-%m-%d %H:%M:%S')
		choice_list = request.POST.getlist('check')
		choice_list = list(filter(filter_fun,choice_list))
		if form.is_valid():
			form = form.save(commit=False)
			form.announce_at = k
			form.created_by = User.objects.get(id=1)
			form.save()
			for i in choice_list:
				choice=Choice()
				choice.poll = Poll.objects.get(id=form.id)
				choice.choice_text = i
				choice.save()
			return redirect(reverse('home'))
	else:
		form = QuestionForm()
	return render(request,'poll/form.html',{'pollform':form})

def poll_list(request):
	polls = Poll.objects.all()
	return render(request,'poll/poll_list.html',{'polls':polls})

def poll_page(request,poll_id):
	poll = Poll.objects.get(id=poll_id)
	choices = Choice.objects.all().filter(poll=poll)
	params = {
		'details':poll.poll_details,
		'choices' : choices,
		'poll':poll
	}
	return render(request,'poll/poll_page.html',params)

def voting(request,poll_id,choice_id):
	message = None
	poll=Poll.objects.get(id=poll_id)
	choice = Choice.objects.all().filter(poll=poll)
	if not poll.voters.all().filter(username=request.user.username).exists():
		Choice.objects.get(id=choice_id).votes += 1
		return redirect('poll_list')
	else:
		return HttpResponse('You have already voted !!!!')
	params = {
		'poll':poll,
		'choices' : choice,
		'message': message,
		'poll':poll
	}
	return render(request,'poll/poll_page.html',params)



