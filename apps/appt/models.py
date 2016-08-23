from __future__ import unicode_literals

from django.db import models
from datetime import datetime, date
# Create your models here.
class ApptManager(models.Manager):
	def create_appt(self, data):
		errors=[]
		if data['date'] == "" or not datetime.now() < datetime.strptime(data['date'], '%Y-%m-%d') or not datetime.now() < datetime.strptime(data['time'], '%H:%i'):
			errors.append("Date may not be blank and should be current or future dated")
		if data['time'] == "":
			errors.append("Time may not be blank")
		if not len(data['tasks']) > 1:
			errors.append("Tasks may not be blank")
		if not errors:
			return(True, data)
		return(False, errors)
	def update_appt(self, id, data):
		appt = Appt.objects.get(id=id)
		errors=[]
		if data['date'] == "" or datetime.strptime(data['date'], '%Y-%m-%d') < datetime.now():
			errors.append("Date may not be blank and should be current or future dated")
		if data['time'] == "":
			errors.append("Time may not be blank")
		if not len(data['tasks']) > 1:
			errors.append("Tasks may not be blank")
		if errors:
			return(False, errors)
		else:
			appt.date = data['date']
			appt.time = data['time']
			appt.tasks = data['tasks']
			appt.status = data['status']
			appt.save()
			return(True, appt)

class Appt(models.Model):
	date = models.DateField()
	time = models.TimeField()
	tasks = models.CharField(max_length=100)
	status = models.CharField(max_length=45)
	user = models.ForeignKey('loginreg.User', related_name="usersappts")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	apptManager = ApptManager()
	objects = models.Manager()