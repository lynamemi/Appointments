from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Appt
from ..loginreg.models import User
from django.contrib import messages
from datetime import datetime, date
# Create your views here.
def index(request):
	return render(request, 'loginreg/loginreg.html')
def show_appt(request):
	try:
		context = {
			'appts':Appt.objects.filter(user_id=request.session['user']).exclude(date=datetime.now()),
			'todays_appts':Appt.objects.filter(date=datetime.now(), user_id=request.session['user'])
			}
		print datetime.now()
		return render(request, 'appt/show_appt.html', context)
	except:
		return render(request, 'appt/show_appt.html')
def edit_appt(request, id):
	context = {
		'appt':Appt.objects.get(id=id)
		}
	return render(request, 'appt/edit_appt.html', context)
def update_appt(request, id):
	if request.method == 'POST':
		updated_appt = Appt.apptManager.update_appt(id, request.POST)
		if updated_appt[0] == False:
			for error in updated_appt[1]:
				messages.add_message(request, messages.INFO, error)
			return redirect(reverse('edit_appt', kwargs={'id':id}))
		else:
			return redirect('/appointments')
	else:
		pass
def add_appt(request):
	new_appt = Appt.apptManager.create_appt(request.POST)
	if new_appt[0] == False:
		for error in new_appt[1]:
			messages.add_message(request, messages.INFO, error)
		return redirect('/appointments')
	else:
		Appt.objects.create(date=request.POST['date'], time=request.POST['time'], tasks=request.POST['tasks'], status="pending", user=User.objects.get(id=request.session['user']))
		return redirect('/appointments')
def delete_appt(request, id):
	appt = Appt.objects.get(id=id)
	appt.delete()
	return redirect('/appointments')
