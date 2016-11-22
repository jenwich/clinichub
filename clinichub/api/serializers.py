from clinichub.models import *
from rest_framework.serializers import *
from rest_framework_mongoengine.serializers import *
from rest_framework.exceptions import *

class ClinicSerializer(DocumentSerializer):
    name = CharField(max_length=50)
    description = CharField(max_length=100, allow_blank=True)
    price = FloatField(min_value=0)

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'description', 'price', 'fields')

class PatientSerializer(DocumentSerializer):
    fullname = ReadOnlyField()
    class Meta:
        model = Patient
        fields = ('id', 'username', 'email', 'firstname', 'lastname', 'fullname', 'birthdate', 'id_no', 'balance', 'phone_no', 'address', 'allergy')

class ClinicPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        clinic = Clinic.objects(id=data).first()
        if not clinic:
            raise NotFound()
        return clinic

    def to_representation(self, obj):
        serializer = ClinicSerializer(obj)
        return serializer.data

class DoctorSerializer(DocumentSerializer):
    fullname = ReadOnlyField()
    clinic = ClinicPrimaryKeyRelatedField(queryset=Clinic.objects, allow_null=True)
    class Meta:
        model = Doctor
        fields = ('id', 'username', 'email', 'firstname', 'lastname', 'fullname', 'birthdate', 'id_no', 'field', 'clinic', 'md_no', 'activate')

class MessageSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Message
        fields = ('msg', 'sender', 'time')

class DoctorPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        doctor = Doctor.objects(id=data).first()
        if not doctor:
            raise NotFound()
        return doctor

    def to_representation(self, obj):
        serializer = DoctorSerializer(obj)
        data = serializer.data
        doctor_include = ['id', 'username', 'fullname', 'field', 'clinic']
        clinic_include = ['id', 'name', 'desciption']
        data = { key: data[key] for key in data if key in doctor_include }
        data['clinic'] = { key: data['clinic'][key] for key in data['clinic'] if key in clinic_include }
        return data

class PatientPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        patient = Patient.objects(id=data).first()
        if not patient:
            raise NotFound()
        return patient

    def to_representation(self, obj):
        serializer = PatientSerializer(obj)
        data = serializer.data
        patient_include = ['id', 'username', 'fullname', 'phone_no']
        data = { key: data[key] for key in data if key in patient_include }
        return  data

class SessionSerializer(DocumentSerializer):
    doctor = DoctorPrimaryKeyRelatedField(queryset=Doctor.objects)
    patient = PatientPrimaryKeyRelatedField(queryset=Patient.objects)
    messages = ListField(child=MessageSerializer())

    class Meta:
        model = Session
        fields = ('id', 'topic', 'doctor', 'patient', 'messages')

class SessionPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        session = Session.objects(id=data).first()
        if not session:
            raise NotFound()
        return session

    def to_representation(self, obj):
        serializer = SessionSerializer(obj)
        data = serializer.data
        session_include = ['id', 'topic']
        data = { key: data[key] for key in data if key in session_include }
        return data

class AppointmentSerializer(DocumentSerializer):
    doctor = DoctorPrimaryKeyRelatedField(queryset=Doctor.objects)
    patient = PatientPrimaryKeyRelatedField(queryset=Patient.objects)
    session = SessionPrimaryKeyRelatedField(queryset=Session.objects)

    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'patient', 'time', 'note', 'location', 'state', 'session')

class DrugSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Drug
        fields = ('name', 'amount', 'usage')

class TranscriptSerializer(DocumentSerializer):
    doctor = DoctorPrimaryKeyRelatedField(queryset=Doctor.objects)
    patient = PatientPrimaryKeyRelatedField(queryset=Patient.objects)
    drugs = ListField(child=DrugSerializer())

    class Meta:
        model = Transcript
        fields = ('id', 'doctor', 'patient', 'note', 'drugs')