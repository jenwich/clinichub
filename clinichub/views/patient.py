from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from clinichub.models import *

def patient_profile(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            return redirect(reverse('patient_info'))
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
                    'doctor': session.doctor.fullname,
                    'clinic': session.doctor.clinic.name,
                    'state': session.state
                } for session in sessions] 
                sessions_active = [ session for session in sessions_ if session['state'] == 'active' ]
                sessions_archive = [ session for session in sessions_ if session['state'] == 'archive' ]
            except Exception as e:
                return render(request, 'patient/sessions.html', {
                    'error_message': e.args[0]
                })
            return render(request, 'patient/sessions.html', {
                'page': 'sessions',
                'sessions': sessions_,
                'sessions_active': sessions_active,
                'sessions_archive': sessions_archive
            })
    else:
        return redirect(reverse('login'))

def patient_info(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            user = Patient.objects(username=request.session.get('username')).first()
            return render(request, 'patient/info.html', {
                'page': 'info',
                'user': user
            })
    else:
        return redirect(reverse('login'))

def patient_payment(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            user = Patient.objects(username=request.session.get('username')).first()
            return render(request, 'patient/payment.html', {
                'user_id': user.id,
                'page': 'payment',
                'balance': user.balance
            })
    else:
        return redirect(reverse('login'))

def patient_appointments(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            try:
                user = Patient.objects(username=request.session.get('username')).first()
                appointments = Appointment.objects(patient=user)
                appointments_ = [{
                    'id': appointment.id, 
                    'doctor': appointment.doctor.username, 
                    'clinic': appointment.doctor.clinic.name, 
                    'time': appointment.time, 
                    'note': appointment.note, 
                } for appointment in appointments]
                return render(request, 'patient/appointments.html', {
                    'page': 'appointments',
                    'appointments': appointments_,
                    'user_id': user.id
                })
            except Exception as e:
                return render(request, 'patient/appointments.html', {
                    'error_message': e.args[0]
                })
    else:
        return redirect(reverse('login'))

def patient_prescriptions(request):
    if 'username' in request.session:
        if request.session.get('user_type') != 'patient':
            return redirect(reverse('doctor_profile'))
        else:
            try:
                user = Patient.objects(username=request.session.get('username')).first()
                prescriptions = Prescription.objects(patient=user)
                prescriptions_ = [{
                    'id': prescription.id, 
                    'doctor': prescription.doctor.fullname, 
                    'clinic': prescription.doctor.clinic.name, 
                    'drugs': prescription.drugs, 
                    'note': prescription.note, 
                } for prescription in prescriptions]
                return render(request, 'patient/prescriptions.html', {
                    'page': 'prescriptions',
                    'prescriptions': prescriptions_
                })
            except Exception as e:
                return render(request, 'patient/prescriptions.html', {
                    'error_message': e.args[0]
                })
    else:
        return redirect(reverse('login'))
