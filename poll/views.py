from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import *
from django.contrib import messages
from django.http import Http404
from basic.models import *
from basic.views import member_check
from basic.utils import *
from .forms import *
from .models import *
from django.utils import timezone
from notifications.signals import notify

@login_required
def polls(request,unique_id,form=None):
	classroom = Classroom.objects.get(unique_id=unique_id)
	if member_check(request.user,classroom):
		polls = Poll.objects.filter(classroom=classroom)
		#handling forms of poll and its choice
		admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
		if admin_check:
			if request.method=='POST':
				form = QuestionForm(request.POST or None,request.FILES)
				choice_list = request.POST.getlist('check')
				choice_list = list(filter(filter_fun,choice_list))
				if form.is_valid():
					form = form.save(commit=False)
					form.classroom = classroom
					form.created_by = request.user
					form.save()
					for i in choice_list:
						choice=Choice()
						choice.poll = Poll.objects.get(id=form.id)
						choice.choice_text = i
						choice.save()
					verb = f'A poll added in f{classroom.class_name}'
					recipients=User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
					url = reverse('poll_page',kwargs={'unique_id':classroom.unique_id,'poll_id':form.id})
					notify.send(sender=request.user,verb=verb,url=url,recipient=recipients)
					return redirect(reverse('polls',kwargs={'unique_id':classroom.unique_id}))
			else:
				form = QuestionForm()

		query,page_range = pagination(request,polls)
		polls=query.object_list
		params = {
			'pollform':form,
			'polls':polls,
			'classroom':classroom,
			'query':query,
			'page_range':page_range,
			'is_admin':admin_check
			}
		return render(request,'poll/polls_list.html',params)

@login_required
def poll_page(request,unique_id, poll_id,form=None):
	classroom = Classroom.objects.get(unique_id = unique_id)
	if member_check(request.user,classroom):
		poll = Poll.objects.get(id=poll_id)
		choices = Choice.objects.all().filter(poll=poll)
		time_up = timezone.now() >= poll.announce_at
		if time_up:
			choices = choices.order_by('-votes')

		admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
		if admin_check:
			if request.method=='POST':
				form = PollUpdateForm(request.POST ,request.FILES,instance=poll)
				if form.is_valid():
					form = form.save(commit=False)
					form.save()
					return redirect(reverse('poll_page',kwargs={'unique_id':classroom.unique_id,'poll_id':poll.id}))
			else:
				form = PollUpdateForm(instance=poll)

		params = {
			'choices' : choices,
			'poll':poll,
			'details':poll.poll_details,
			'classroom':classroom,
			'show_result': time_up or poll.voters.filter(username=request.user.username).exists(),
			'voters_length':poll.voters.count(),
			'updateform':form,
			'is_admin':admin_check,
		}
		if poll.file:
			params['extension']=extension_type(poll.file)
		return render(request,'poll/poll_details.html',params)

@login_required
def voting(request,unique_id,poll_id,choice_id):
	classroom = Classroom.objects.get(unique_id = unique_id)
	poll=Poll.objects.get(id=poll_id)
	url = reverse('poll_page',kwargs={'unique_id':classroom.unique_id,'poll_id':poll.id})
	if member_check(request.user,classroom):
		choice = Choice.objects.filter(poll=poll)
		if poll.who_can_vote=='Students':
			members = classroom.members.all()
			teachers = classroom.teacher.all()
			students = members.difference(teachers)
			if request.user not in students:
				messages.add_message(request,messages.INFO,f'Only Students are allowed to Vote.')
				return redirect(url)

		if timezone.now() <= poll.announce_at:
			if poll.voters.filter(username=request.user.username).exists():
				messages.add_message(request,messages.INFO,"You have already voted.")
				return redirect(url)
			else:
				choice=Choice.objects.get(id=choice_id)
				choice.votes += 1
				poll.voters.add(request.user)
				choice.save()
		else:
			messages.add_message(request,messages.INFO,"Time's up for voting")
			return redirect(url)

@login_required
def delete_poll(request,unique_id, poll_id):
	classroom = get_object_or_404(Classroom,unique_id = unique_id)
	poll = get_object_or_404(Poll,id=poll_id)
	if request.user == poll.created_by:
		poll.delete()
		return redirect(reverse('polls',kwargs={'unique_id':classroom.unique_id}))
	else:
		raise Http404()