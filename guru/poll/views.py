from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import *
from django.contrib import messages

from basic.models import *
from basic.views import member_check
from basic.utils import *
from .forms import *
from .models import *
from django.utils import timezone

def filter_fun(key):
	return key!=""

@login_required
def polls(request,unique_id):
	classroom = Classroom.objects.get(unique_id=unique_id)
	if member_check(request.user,classroom):
		polls = Poll.objects.all()
		my_classes = Classroom.objects.all().filter(members=request.user)
		#handling forms of poll and its choice
		if request.method=='POST':
			form = QuestionForm(request.POST or None,request.FILES)
			choice_list = request.POST.getlist('check')
			choice_list = list(filter(filter_fun,choice_list))

			if form.is_valid():
				form = form.save(commit=False)
				form.classroom = classroom
				form.announce_at = request.POST.get('date')
				form.created_by = request.user
				form.save()

				for i in choice_list:
					choice=Choice()
					choice.poll = Poll.objects.get(id=form.id)
					choice.choice_text = i
					choice.save()
				return redirect(f'/polls/{unique_id}')
		else:
			form = QuestionForm()

		query,page_range = pagination(request,polls)
		polls=query.object_list
		classes = Classroom.objects.filter(members=request.user)
		params = {
			'pollform':form,
			'polls':polls,
			'classroom':classroom,
			'classes':my_classes,
			'query':query,
			'page_range':page_range,
			'classes':classes
			}
		return render(request,'poll/polls_list.html',params)

def poll_page(request,unique_id, poll_id):
	classroom = Classroom.objects.get(unique_id = unique_id)
	if member_check(request.user,classroom):
		now = timezone.now()
		#poll list and voting page.
		poll = Poll.objects.get(id=poll_id)
		choices = Choice.objects.all().filter(poll=poll)
		if now >= poll.announce_at:
			choices = choices.order_by('-votes')
		voters = poll.voters.count()
		my_classes = Classroom.objects.all().filter(members=request.user)

		if request.method=='POST':
			form = QuestionForm(request.POST or None,request.FILES,instance=poll)

			if form.is_valid():
				form = form.save(commit=False)
				form.announce_at = request.POST.get('date')
				form.save()
				return redirect(f'/polls/{unique_id}/poll-page/{poll.id}')
		else:
			form = QuestionForm(instance=poll)
		members_email = classroom.members.values_list('email', flat=True)
		teachers_email = classroom.teacher.values_list('email', flat=True)
		params = {
			'details':poll.poll_details,
			'choices' : choices,
			'poll':poll,
			'classroom':classroom,
			'show_result': now >= poll.announce_at,
			'voters_length':voters,
			'classes':my_classes,
			'updateform':form,
			'emails':members_email,
			'members_email':members_email,
			'teachers_email':teachers_email
		}
		if poll.voters.filter(username=request.user.username).exists():
			params['classes'] = Classroom.objects.all().filter(members=request.user)
		if poll.file:
			params['extension']=extension_type(poll.file)

		return render(request,'poll/poll_details.html',params)

def voting(request,unique_id,poll_id,choice_id):
	classroom = Classroom.objects.get(unique_id = unique_id)
	if member_check(request.user,classroom):
		message = None
		poll=Poll.objects.get(id=poll_id)
		choice = Choice.objects.all().filter(poll=poll)
		who_can_vote = poll.who_can_vote

		if who_can_vote=='Students':
			members = classroom.members.all()
			teachers = classroom.teacher.all()
			students = members.difference(teachers)
			if request.user not in students:
				messages.add_message(request,messages.INFO,f'Only Students are allowed to Vote.')
				return redirect(f'/polls/{unique_id}/poll-page/{poll.id}')

		now = timezone.now()
		can_vote_now = now <= poll.announce_at
		if can_vote_now:
			if not poll.voters.filter(username=request.user.username).exists():
				choice=Choice.objects.get(id=choice_id)
				choice.votes += 1
				poll.voters.add(request.user)
				choice.save()
				return redirect(f'/polls/{unique_id}/poll-page/{poll.id}')
			else:
				messages.add_message(request,messages.INFO,"You have already voted.")
				return redirect(f'/polls/{unique_id}/poll-page/{poll.id}')
		else:
			messages.add_message(request,messages.INFO,"Time's up for voting")
			return redirect(f'/polls/{unique_id}/poll-page/{poll.id}')

def delete_poll(request,unique_id, poll_id):
	poll = Poll.objects.get(id=poll_id)
	if request.user == poll.created_by:
		poll.delete()
		return redirect(f'/polls/{unique_id}')
	else:
		raise Http404()



