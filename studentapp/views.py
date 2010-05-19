# Views for StudentApp Application
from google.appengine.api import users
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import modelformset_factory, inlineformset_factory
import models
from busticket.models import Events
import forms
import datetime
import atom
import gdata.service
import gdata.auth
import gdata.alt.appengine
import gdata.calendar
import gdata.calendar.service

# View methods begin here

def edit_student(request, student_id=None):
    #TODO: Get Avatar Upload Working
    if request.method == 'POST':
        if student_id:
            # This pulls up the current student for editing
            student = models.StudentInfo.get_by_id(int(student_id))
            add_form = forms.StudentForm(request.POST, instance=student)
        else:
            add_form = forms.StudentForm(request.POST)
        if add_form.is_valid():
            student = add_form.save(commit=False)
            student.userID = users.get_current_user()
            student.put()
            return HttpResponseRedirect('/student/')
    else:
        if student_id:
            student = models.StudentInfo.get_by_id(int(student_id))
            add_form = forms.StudentForm(instance=student)
        else:
            StudentFormset = inlineformset_factory(models.StudentInfo, models.StudentAvatar)
            formset = StudentFormset()
    return render_to_response('studentapp/studentform.html', {
        'student_id' : student_id,
        'student_form' : formset,
    })

def display_student_data(request):
    current_student = users.get_current_user()
    student_data = models.StudentInfo.all().filter('userID =', current_student).get()
    if student_data:
        #TODO: Get Avatar Working Here.
        #TODO: This is where student calendar, documents in progress, points, etc. will be retrieved.
        #TODO: Collect Event Data for Context.
        return render_to_response('studentapp/studentprofile.html', {
            'student_name' : current_student.nickname(),
            'student_data' : student_data,
        })
    else:
        return HttpResponseRedirect('/student/edit/')