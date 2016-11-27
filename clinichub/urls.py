from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from . import views

patient_urlpatterns = [
    url(r'^$', views.patient_profile, name='patient_profile'),
    url(r'^sessions$', views.patient_sessions, name='patient_sessions'),
    url(r'^info$', views.patient_info, name='patient_info'),
    url(r'^payment$', views.patient_payment, name='patient_payment'),
    url(r'^appointments$', views.patient_appointments, name='patient_appointments'),
    url(r'^prescriptions$', views.patient_prescriptions, name='patient_prescriptions'),
]

doctor_urlpatterns = [
    url(r'^$', views.doctor_profile, name='doctor_profile'),
    url(r'^sessions$', views.doctor_sessions, name='doctor_sessions'),
    url(r'^info$', views.doctor_info, name='doctor_info'),
    url(r'^clinic$', views.doctor_clinic, name='doctor_clinic'),
    url(r'^create_clinic$', views.doctor_create_clinic, name='doctor_create_clinic'),
    url(r'^appointments$', views.doctor_appointments, name='doctor_appointments'),
]

session_urlpatterns = [
    url(r'^create$', views.session_create, name='session_create'),
    url(r'^(?P<session_id>[a-f0-9]{24})$', views.session, name='session'),
]

prescription_urlpatterns = [
    url(r'^(?P<prescription_id>[a-f0-9]{24})$', views.prescription, name='prescription'),
]

appointment_urlpatterns = [
    url(r'^(?P<appointment_id>[a-f0-9]{24})$', views.appointment, name='appointment'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile/', include(patient_urlpatterns)),
    url(r'^doctor$', views.doctor_index, name='doctor_index'),
    url(r'^doctor/login$', views.doctor_login, name='doctor_login'),
    url(r'^doctor/register$', views.doctor_register, name='doctor_register'),
    url(r'^doctor/profile/', include(doctor_urlpatterns)),
    url(r'^session/', include(session_urlpatterns)),
    url(r'^prescription/', include(prescription_urlpatterns)),
    url(r'^appointment/', include(appointment_urlpatterns)),
    url(r'^api/', include('clinichub.api.urls')),
]
