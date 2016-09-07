from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages

# Create your views here.
def loginreg(request):
	return render(request, 'loginreg/loginreg.html')
def reg_process(request):
	reg_user = User.userManager.register(request.POST)
	if reg_user[0] == False:
		for error in reg_user[1]:
			messages.add_message(request, messages.INFO, error)
		return redirect(reverse('main'))
	else:
		request.session['user'] = reg_user[1].id
		request.session['first_name'] = reg_user[1].first_name
		print request.session['first_name']
		print request.session['user']
	return redirect(reverse('show_appt'))
def log_process(request):
	log_user = User.userManager.login(request.POST)
	if log_user[0] == False:
		messages.add_message(request, messages.INFO, log_user[1])
		return redirect(reverse('main'))
	else:
		request.session['id'] = log_user[1].id
		return redirect(reverse('show_appt'))
def logout(request):
	try:
		request.session.clear()
	except:
		pass
	return redirect('/')