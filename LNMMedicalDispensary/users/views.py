from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login

from .models import *
from .forms import *
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
#from user_profile.models import UserProfile
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            msg = 'user created'
            patient=Patient(Pid=request.user.id,name=user.username,age=user.age,gender=user.gender)
            patient.save()
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_doctor:
                login(request, user)
                return redirect('doctor')
            elif user is not None and user.is_chemist:
                login(request, user)
                return redirect('chemist')
            elif user is not None and user.patient:

                login(request, user)
                return redirect('patient')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def doctor(request):
    return render(request, 'doctor.html')


def chemist(request):
    return render(request, 'chemist.html')


def patient(request):
    return render(request, 'patient.html')


def scheduleTest(request):
    return render(request, 'scheduleTest.html')


#def patientHistory(request):
 #   return render(request, 'PatientHistory.html')




def viewPatientHistory(request):
    return render(request, 'viewPatientHistory.html')


def feedback(request):
    return render(request, 'feedback.html')


def patientProfile(request):
    return render(request, 'PatientProfile.html')


def bookAppointment(request):
    return render(request, 'bookAppointment.html')


def checkAppointment(request):
    appointment=Appointment.objects.all()
    Appointments=[{}]
    sr=1
    
    for i in appointment:
        Appointments.insert(sr-1,{'sr':sr,'Timings':i.Timings,'name':Patient.objects.get(Pid=i.Pid.Pid).name,'mailid':i.mailid})
        sr=sr+1
    Appointments.pop()
    print(len(Appointments))  
    
    #print(request.GET['cancel'])
    #patient=Patient.objects.get()
    return render(request, 'checkAppointment.html',{'Appointments': Appointments})


def Treatment(request):
    return render(request, 'Treatment.html')


def DoctorProfile(request):
    return render(request, 'DoctorProfile.html')


def ChemistProfile(request):
    return render(request, 'chemistProfile.html')


def checkMedicine(request):
    return render(request, 'checkMedicine.html')


def MedicineRecord(request):
    return render(request, 'medicineRecord.html')


def issueMedicine(request):
    return render(request, 'issueMedicine.html')


# appointment booking 
@login_required(login_url='/login/')
def RequestAppointment(request):
    current_user = request.user
    id=current_user.id-2

    try:
        doctor=request.GET["D_name"]
    except MultiValueDictKeyError:
        doctor = False
    try:
        timings=request.GET["meeting-time"]
    except MultiValueDictKeyError:
        timings = False
    try:
        Mailid=request.GET["mailid"]
    except MultiValueDictKeyError:
        Mailid = False
    
    pid=Patient.objects.get(Pid=id)
    
    did=Doctor.objects.get(name=doctor)
    print(pid)
    print(did)
    print(timings)
    
    p= Appointment(Pid=pid,Did=did,Timings=timings,mailid=Mailid)
    p.save()
    return render(request,'RequestAppointment.html')
   
# update patient profile
def updatepatient(request):
    current_user = request.user
    
    pid=current_user.id-2
    print(current_user)
    print(pid)

    try:
        name = request.GET["name"]
        
    except MultiValueDictKeyError:
        name = False
    try:
        age = request.GET["age"]
        
    except MultiValueDictKeyError:
        age = False
    try:
        gender = request.GET["gender"]
        
    except MultiValueDictKeyError:
        gender = False
        
    p=Patient.objects.get(Pid=pid)   
    p.name=name
    p.age=age
    p.gender=gender
    p.save()
    return render(request,'UpdatepatientProfile.html')


# pateint history
def patientHistory(request):
    my_history=PatientHistory.objects.filter(Pid=request.user.id-2)
    print(request.user.id)
        
    context={'my_his':my_history}
    return render(request, 'PatientHistory.html',context)


# schedule test
def TestSchedule(request):
    return render(request,'TestSchedule.html')