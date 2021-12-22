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
            
           
            p=patient.objects.get(name=user.name)
            p.Pid=user.Uid
            p.save()
            msg = 'user created'
            # patient = Patient( name=user.username, age=user.age, gender=user.gender)
            # patient.save()
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
                print(user.name)
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


def MedicalCertificate(request):
    doctor= Doctor.objects.all()
    for i in Doctor.objects.all():
       print(i)
    current_user = request.user
    id=current_user.uid

    try:
        doctorid=request.GET["doctor"]
    except MultiValueDictKeyError:
        doctorid = False
    
    print(doctorid)
    
    context = { 'doctors' : doctor}
    pid=Patient.objects.get(Pid=id)
    
    did=Doctor.objects.get(name=doctorid)
    medical=MedicalCertificate(Pid=pid,Did=did,fromdate=request.GET["start"],todate=request.GET["end"],reason=request.POST["reason"])
    medical.save()
    print("success")
    return render(request, 'MedicalCertificate.html', context)


def feedback(request):

    if request.method == 'POST' :
        try:
            doctorid=request.POST["doctor"]
            feedbackBody = request.POST["subject"]
        except MultiValueDictKeyError:
            doctorid = False
            mailID = False
            feedbackBody = False
        
        print("doctor ID = ", doctorid)
        #print("mailID = ", mailID)
        print("feedback body = ", feedbackBody)
        patient = Patient.objects.get(Pid=request.user.uid)
        doctor = Doctor.objects.get(Did=doctorid)
        feedbackInstance = Feedback.objects.create(doctor=doctor,patient=patient, feedback=feedbackBody)

        return redirect("patient")

    else: 
        doctorChoices = Doctor.objects.all()
        context = {'doctorChoices' : doctorChoices}
        return render(request, 'feedback.html', context)



# def patientHistory(request):
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
    appointment = Appointment.objects.all()
    Appointments = [{}]
    sr = 1
    user = request.user
    for i in appointment:
        if i.Did.Did == user.uid:
            Appointments.insert(sr-1, {'sr': sr, 'Timings': i.Timings,
                                       'name': Patient.objects.get(Pid=i.Pid.Pid).name, 'mailid': i.mailid})
            sr = sr+1
    Appointments.pop()
    print(len(Appointments))

    # print(request.GET['cancel'])
    # patient=Patient.objects.get()
    return render(request, 'checkAppointment.html', {'Appointments': Appointments})


def Treatment(request):
    return render(request, 'Treatment.html')


def DoctorProfile(request):
    user = request.user
    print(user)
    doctor = Doctor.objects.all()
    # sr = 1
    profile = [{}]
    for i in doctor:
        if i.Did == user.id:
            p = dict({'name': i.name, 'did': i.Did,
                      'age': i.age, 'Gender': i.gender, 'address': i.address, 'speciality': i.speciality, 'ph': i.phonenumber})
            profile.insert(0, p)
            break
    # profile.pop()
    # print(profile)
    # profile=Doctor.objects.get(Did=user.id)
    return render(request, 'DoctorProfile.html', {'profile': profile[0]})


def ChemistProfile(request):
    user = request.user
    form = ChemistForm(instance=user)
    if request.method == 'POST':
        # The request.POST data will be send to the project instance
        form = ChemistForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # IT will modify the project
            # signal for profile updated to be put
            # user will be redirected to the projects page
            return redirect('chemistProfile')

    context = {'form': form, 'user': user}
    return render(request, 'chemistProfile.html', context)


def checkMedicine(request):
    form = MedicineForm()
    medicine = Medicine.objects.all()
    if request.method == 'POST':
       # print(request.POST)  # So we see its a dictionary of attributes of project and its details
        form = MedicineForm(request.POST, request.FILES)
        # if form.is_valid():
        # form.save()
        # user will be redirected to the projects page
        return redirect('updateMedicine', request.POST['Mid'])

    context = {'form': form, 'medicines': medicine}
    return render(request, 'checkMedicine.html', context)


def updateMedicine(request, pk):
    current_medicine = Medicine.objects.get(Mid=pk)
    medicine = Medicine.objects.all()
    # print(medicine)
    form = MedicineInstance(instance=current_medicine)
    if request.method == 'POST':
        # The request.POST data will be send to the project instance
        form = MedicineInstance(
            request.POST, request.FILES, instance=current_medicine)
        if form.is_valid():
            form.save()  # IT will modify the project
            # user will be redirected to the projects page
            return redirect('checkMedicine')
    context = {'form': form, 'medicines': medicine}
    return render(request, "updateMedicine.html", context)


def MedicineRecord(request):
    medicine = Medicine.objects.all()
    # for i in medicine:
    # print(medicine)
    context = {'medicines': medicine}

    return render(request, 'medicineRecord.html', context)


def issueMedicine(request):
    form = IssueMedicineForm()
    if request.method == 'POST':
       # print(request.POST)  # So we see its a dictionary of attributes of project and its details
        form = IssueMedicineForm(request.POST, request.FILES)
        # if form.is_valid():
        try:
            med = request.POST['medicine']
        except MultiValueDictKeyError:
            med = False
        medicine = Medicine.objects.get(Mid=med)
        Qy = int(medicine.Quantity)
        try:
            qy = int(request.POST['quantity'])
        except MultiValueDictKeyError:
            qy = False

        if Qy >= qy:
            medicine.Quantity = Qy - qy
            medicine.save()
            form.save()
            # Signal for medicine issued
        else:
            print('Hello')
            # signal for wrong quantity input
        redirect('issueMedicine')

    context = {'form': form}
    return render(request, 'issueMedicine.html', context)


# appointment booking
@login_required(login_url='/login/')
def RequestAppointment(request):
    current_user = request.user
    id = current_user.uid

    try:
        doctor = request.GET["D_name"]
    except MultiValueDictKeyError:
        doctor = False
    try:
        timings = request.GET["meeting-time"]
    except MultiValueDictKeyError:
        timings = False
    try:
        Mailid = request.GET["mailid"]
    except MultiValueDictKeyError:
        Mailid = False

    pid = Patient.objects.get(Pid=id)

    did = Doctor.objects.get(name=doctor)
    print(pid)
    print(did)
    print(timings)

    p = Appointment(Pid=pid, Did=did, Timings=timings, mailid=Mailid)
    p.save()
    return render(request, 'RequestAppointment.html')

# update patient profile


def updatepatient(request):
    current_user = request.user

    pid = current_user.uid
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

    p = Patient.objects.get(Pid=pid)
    p.name = name
    p.age = age
    p.gender = gender
    p.save()
    return render(request, 'UpdatepatientProfile.html')


# pateint history
def patientHistory(request):
    print(request.user.uid)
    my_history = None
    pat = None
    if request.user.patient == True:
        my_history = PatientHistory.objects.filter(Pid=request.user.uid)

        pat = Patient.objects.get(Pid=request.user.uid)
    else:
        id = request.GET['patid']
        my_history = PatientHistory.objects.filter(Pid=id)
        pat = Patient.objects.filter(Pid=id).first()

    # print(request.user.id)

    context = {'my_his': my_history, 'my_pat': pat}
    return render(request, 'PatientHistory.html', context)





# schedule test

    # current_medicine = request.Medicine

    # mid=current_medicine.Mid
    # name=current_medicine.Name
    # type=current_medicine.Type
    # quantity=current_medicine.Quantity
    # usage=current_medicine.Usage
    # supplier=current_medicine.Supplier
    # purchaseDate=current_medicine.PurchaseDate
    # expiryDate=current_medicine.ExpiryDate

    # print(current_medicine)
    # print(mid)

    # try:
    #     name = request.GET["Name"]

    # except MultiValueDictKeyError:
    #     name = False
    # try:
    #     type = request.GET["Type"]

    # except MultiValueDictKeyError:
    #     type = False
    # try:
    #     quantity = request.GET["Quantity"]

    # except MultiValueDictKeyError:
    #     quantity = False

    # try:
    #     usage = request.GET["Usage"]

    # except MultiValueDictKeyError:
    #     usage = False

    # try:
    #     supplier = request.GET["Supplier"]

    # except MultiValueDictKeyError:
    #     supplier = False

    # try:
    #     purchaseDate = request.GET["PurchaseDate"]

    # except MultiValueDictKeyError:
    #     purchaseDate = False

    # try:
    #     expiryDate = request.GET["ExpiryDate"]

    # except MultiValueDictKeyError:
    #     expiryDate = False

    # p=Medicine.objects.get(Mid=mid)
    # p.Name=name
    # p.Type=type
    # p.Quantity=quantity
    # p.Usage=usage
    # p.Supplier=supplier
    # p.PurchaseDate=purchaseDate
    # p.ExpiryDate=expiryDate
    # p.save()
    # return render(request,'checkMedicine.html')
