from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from clinichub.models import *

def patient_profile(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return render(request, 'patient/profile.html', {
                'page': 'profile',
            })
    else:
        return redirect(reverse('login'))

def patient_sessions(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            try:
                user = Patient.objects(username=request.session.get('username')).first()
                sessions = Session.objects(patient=user)
                sessions_ = [{
                    'id': session.id,
                    'topic': session.topic,
                    'doctor': session.doctor.username,
                    'clinic': session.doctor.clinic.name
                } for session in sessions] 
            except Exception as e:
                raise
            return render(request, 'patient/sessions.html', {
                'page': 'sessions',
                'sessions': sessions_
            })
    else:
        return redirect(reverse('login'))

def patient_info(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return render(request, 'patient/info.html', {
                'page': 'info',
            })
    else:
        return redirect(reverse('login'))

def patient_payment(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return render(request, 'patient/payment.html', {
                'page': 'payment',
            })
    else:
        return redirect(reverse('login'))

def patient_appointments(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return render(request, 'patient/appointments.html', {
                'page': 'appointments',
            })
    else:
        return redirect(reverse('login'))

def patient_transcripts(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return render(request, 'patient/transcripts.html', {
                'page': 'transcripts',
            })
    else:
        return redirect(reverse('login'))
