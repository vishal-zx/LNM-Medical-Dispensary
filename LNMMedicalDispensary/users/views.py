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
# from user_profile.models import UserProfile
# Create your views here.
from django.contrib import messages  # for flash messages


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

           # p=patient.objects.get(name=user.name)
            # p.Pid=user.Uid
            # p.save()
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
                # print(user.name)
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


def MedicalCertificateFunction(request):

    current_user = request.user
    id = current_user.Uid
    if request.method == 'POST':
        try:
            dr = request.POST["doctor"]
            Reason = request.POST["reason"]
            fromdate = request.POST["start"]
            todate = request.POST["end"]
        except MultiValueDictKeyError:
            dr = False
            Reason = False
            fromdate = False
            todate = False

        doctorInstance = Doctor.objects.get(Uid=dr)
        Pt = Patient.objects.get(Uid=id)
        print(Pt)
        print(doctorInstance)
        medical = Medicalcertificate.objects.create(
            patient=Pt, doctor=doctorInstance, fromdate=fromdate, todate=todate, reason=Reason)
        print("success")
        # flash message for medicine added succefully
        messages.success(request, 'Medical Certificate Requested Successfully')
        return redirect('patient')
    else:
        doctor = Doctor.objects.all()
        for d in doctor:
            print(d.Uid)
        context = {'doctors': doctor}

        return render(request, 'MedicalCertificate.html', context)

def checkAppointmentStatus(request):
    checkApp = None
    pat = Patient.objects.get(Uid=request.user.Uid)
    checkApp = Appointment.objects.filter(Pid=pat)
    print(checkApp)
    return render(request, 'checkAppointmentStatus.html', {'checkApp': checkApp})

def checkMedicalCertificateStatus(request):
    MedCertis = None
    pat = Patient.objects.get(Uid=request.user.Uid)
    MedCertis = Medicalcertificate.objects.filter(patient=pat)
    print(MedCertis)
    return render(request, 'checkMedicalCertificateStatus.html', {'MedCert': MedCertis})


def viewMedicalCertificateFunction(request):

    if 'Approve' in request.POST:
        try:
            approve = request.POST['Approve']
        except MultiValueDictKeyError:
            approve = None

        print(approve)
        if approve:

            ap = Medicalcertificate.objects.get(medicalID=approve)
            ap.status = 'A'
            ap.save()
        return redirect('viewMedicalCertificate')
    elif 'Reject' in request.POST:
        try:
            reject = request.POST['Reject']
        except MultiValueDictKeyError:
            reject = None

        print(reject)
        if reject:

            ap = Medicalcertificate.objects.get(medicalID=reject)
            ap.status = 'R'
            ap.save()
        return redirect('viewMedicalCertificate')
    else:
        MedCertis = None
        doc = Doctor.objects.get(Uid=request.user.Uid)
        MedCertis = Medicalcertificate.objects.filter(doctor=doc, status='P')
        print(MedCertis)
        return render(request, 'viewMedicalCertificate.html', {'MedCert': MedCertis})


def feedback(request):

    if request.method == 'POST':
        try:
            doctorid = request.POST["doctor"]
            feedbackBody = request.POST["subject"]
        except MultiValueDictKeyError:
            doctorid = False
            mailID = False
            feedbackBody = False

        print("doctor ID = ", doctorid)
        # print("mailID = ", mailID)
        print("feedback body = ", feedbackBody)
        patient = Patient.objects.get(Uid=request.user.Uid)
        doctor = Doctor.objects.get(Uid=doctorid)
        feedbackInstance = Feedback.objects.create(
            doctor=doctor, patient=patient, feedback=feedbackBody)
        # flash message for medicine added succefully
        messages.success(request, 'Feedback Added Successfully')
        return redirect("patient")

    else:
        doctorChoices = Doctor.objects.all()
        context = {'doctorChoices': doctorChoices}
        return render(request, 'feedback.html', context)


# def patientHistory(request):
 #   return render(request, 'PatientHistory.html')


def viewPatientHistory(request):
    # if request.method == 'POST':
    #     id = request.POST['patid']
    #     print(id)
    #     p=Patient.objects.get(Uid=id)
    #     my_history = PatientHistory.objects.filter(Pid=p)
    #     pat = Patient.objects.filter(Uid=id).first()
    #     context = {'my_his': my_history, 'my_pat': pat}
    #     return render(request, 'PatientHistory.html',context)
    # else:
    patient = Patient.objects.all()
    context = {'patient': patient}
    return render(request, 'viewPatientHistory.html', context)


def patientProfile(request):
    user = request.user
    print(user.username)
    patient = Patient.objects.all()
    profile = [{}]
    for i in patient:
        if i.Uid == user.Uid:
            p = dict({'name': user.username, 'pid': i.Pid,
                      'age': i.age, 'ph': i.phonenumber})
            profile.insert(0, p)
    return render(request, 'PatientProfile.html', {'profile': profile[0]})


def bookAppointment(request):
    current_user = request.user
    id = current_user.Uid
    if request.method == 'POST':
        try:
            doctor = request.POST["doctor"]
        except MultiValueDictKeyError:
            doctor = False
        try:
            timings = request.POST["meeting-time"]
        except MultiValueDictKeyError:
            timings = False
        try:
            Mailid = request.POST["mailid"]
        except MultiValueDictKeyError:
            Mailid = False

        pid = Patient.objects.get(Uid=id)

        did = Doctor.objects.get(Uid=doctor)
        print(pid)
        # print(did)
        print(timings)

        Appointment.objects.create(
            Pid=pid, Did=did, Timings=timings, mailid=Mailid)
        messages.success(request, 'Appointent Booked Successfully')
        return render(request, 'Patient.html')
    else:
        doctor = Doctor.objects.all()
        context = {'doctors': doctor}
        return render(request, 'bookAppointment.html', context)


def checkAppointment(request):
    Appointments = [{}]
    if 'cancel' in request.POST:
        try:
            cancel = request.POST['cancel']
        except MultiValueDictKeyError:
            cancel = None

        print(cancel)
        if cancel:

            ap = Appointment.objects.get(Aid=cancel)
            ap.isApproved=False
            ap.save()
        return redirect('checkAppointment')

    else:
        appointment = Appointment.objects.all()

        sr = 1
        doctor = Doctor.objects.get(Uid=request.user.Uid)
    # user = request.user
        for i in appointment:
            if i.Did == doctor:
                Appointments.insert(sr-1, {'sr': sr, 'Timings': i.Timings,
                                           'name': Patient.objects.get(Uid=i.Pid.Uid).name,'isApproved': i.isApproved, 'mailid': i.mailid, 'Aid': i.Aid})
                sr = sr+1
        Appointments.pop()

    # print(request.GET['cancel'])
    # patient=Patient.objects.get()
        return render(request, 'checkAppointment.html', {'Appointments': Appointments})


def Treatment(request):
    if request.method == 'POST':
        try:
            desc = request.POST['descc']
            app = request.POST['appointment']
            print(desc, app)
        except MultiValueDictKeyError:
            desc = False
            app = False
        p = Appointment.objects.get(Aid=app)
        x = Patient.objects.get(Uid=p.Pid.Uid)
        PatientHistory.objects.create(
            Aid=p, Description=desc, Pid=x)
        # flash message for medicine added succefully
        messages.success(request, 'Treatment Given Successfully')
        return render(request, 'Doctor.html')
    else:
        d = Doctor.objects.get(Uid=request.user.Uid)
        appointments = Appointment.objects.filter(Did=d)
        print(appointments)
        context = {'appointment': appointments}
        return render(request, 'Treatment.html', context)


def ViewFeedback(request):
    Feedbacks = None
    feedback = Feedback.objects.all()

    sr = 1
    doc = Doctor.objects.get(Uid=request.user.Uid)
    # user = request.user
    Feedbacks = Feedback.objects.filter(doctor=doc)
    print(Feedbacks)
    return render(request, 'ViewFeedback.html', {'Feedback': Feedbacks})


def DoctorProfile(request):
    user = request.user
    print(user.username)
    doctor = Doctor.objects.all()
    # sr = 1
    profile = [{}]
    for i in doctor:
        if i.Uid == user.Uid:
            p = dict({'name': user.username, 'did': i.Did,
                      'age': i.age, 'gender': i.gender, 'schedule': i.schedule, 'address': i.address, 'speciality': i.speciality, 'ph': i.phonenumber})
            profile.insert(0, p)
            # break
    # profile.pop()
    # print(profile)
    # profile=Doctor.objects.get(Did=user.id)
    return render(request, 'DoctorProfile.html', {'profile': profile[0]})


def ChemistProfile(request):
    # user = request.user
    # form = ChemistForm(instance=user)
    print('Here')
    user = request.user
    uuser = User.objects.get(Uid=user.Uid)
    # chemist = Chemist.objects.get(Uid=user.Uid)
    # form = ChemistForm(instance=chemist)
    print(uuser.phonenumber)
    form = ChemistForm(instance=user)
    if request.method == 'POST':
        print('POST REQUEST')
        # The request.POST data will be send to the project instance
        form = ChemistForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                age = request.POST['age']
                phonenumber = request.POST['phonenumber']
                gender = request.POST['gender']
            except MultiValueDictKeyError:
                age = False
                phonenumber = False
                gender = False
            uuser.age = age
            uuser.phonenumber = phonenumber
            uuser.gender = gender
            uuser.save()
            form.save()
        # if form.is_valid():
            # form.save()  # IT will modify the project
        # currrent_user = User.objects.get(Uid = user.Uid)
            # gender = False
        # currrent_user.age = age
        # currrent_user.phonenumber = phonenumber
        # currrent_user.gender = gender
        # currrent_user.save()
            print('Chemist user updated')
            messages.success(request, 'Chemist Profile Updated Successfully')
            # signal for profile updated to be put
            # user will be redirected to the projects page
        return redirect('chemist')

    context = {'form': form}
    return render(request, 'chemistProfile.html', context)


def addMedicine(request):
    form = MedicineInstance()
    # form = MedicineInstance(request.POST, request.FILES)

    if request.method == 'POST':
        form = MedicineInstance(request.POST, request.FILES)
        try:
            name = request.POST['Name']
            type = request.POST['Type']
            quantity = request.POST['Quantity']
            usage = request.POST['Usage']
            supplier = request.POST['Supplier']
            purchaseDate = request.POST['PurchaseDate']
            expiryDate = request.POST['ExpiryDate']

        except MultiValueDictKeyError:
            name = False
            type = False
            quantity = False
            usage = False
            supplier = False
            purchaseDate = False
            expiryDate = False

        medicine = Medicine.objects.create(Name=name, Type=type, Quantity=quantity,
                                           Usage=usage, Supplier=supplier, PurchaseDate=purchaseDate, ExpiryDate=expiryDate)
        # flash message for medicine added succefully
        messages.success(request, 'Medicine Added Successfully')
        return redirect('chemist')
    context = {'form': form}
    return render(request, 'addMedicine.html', context)


def checkMedicine(request):
    form = MedicineForm()
    medicine = Medicine.objects.all()
    if request.method == 'POST':
       # print(request.POST)  # So we see its a dictionary of attributes of project and its details
        form = MedicineForm(request.POST, request.FILES)
        # if form.is_valid():
        # form.save()
        # user will be redirected to the projects page
        try:
            med = request.POST['Name']
        except MultiValueDictKeyError:
            med = 'error'  # Random name which cant be medicine name
        print('Hello')
        try:
            trialmed = Medicine.objects.get(Name=med)
        except Medicine.DoesNotExist:
            trialmed = False
            # Flash message to be added
            messages.error(request, 'No such medicine found')
            print('no such medicine found')
            return redirect('checkMedicine')

        return redirect('updateMedicine', med)

    context = {'form': form, 'medicines': medicine}
    return render(request, 'checkMedicine.html', context)


def updateMedicine(request, pk):
    # try:
    current_medicine = Medicine.objects.get(Name=pk)
    # except Medicine.DoesNotExist:
    #     # Flash message to be added
    #     print('no such medicine found')
    #     redirect('checkMedicine')
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
            # flash message medicine added successfully
            messages.success(request, 'Updated Successfully')
            return redirect('chemist')
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
            messages.success(request, 'Medicine issued successfully')
            # Signal for medicine issued
        else:
            print('Hello')
            messages.error(request, 'Invalid Quantity')
            # signal for wrong quantity input
        redirect('issueMedicine')

    context = {'form': form}
    return render(request, 'issueMedicine.html', context)


# update patient profile


def updatepatient(request):
    current_user = request.user

    pid = current_user.Uid
    print(current_user)
    print(pid)
    try:
        age = request.GET["age"]

    except MultiValueDictKeyError:
        age = False

    try:
        ph = request.GET["phno"]

    except MultiValueDictKeyError:
        ph = False

    p = Patient.objects.get(Uid=pid)
    # p.name = name
    p.age = age
    p.phonenumber = ph
    p.save()
    messages.success(request, 'Profile updated successfully')
    return render(request, 'Patient.html')


def updatedoctor(request):
    current_user = request.user

    Did = current_user.Uid
    print(current_user)
    print(Did)

    try:
        age = request.GET["age"]

    except MultiValueDictKeyError:
        age = False

    try:
        address = request.GET["address"]

    except MultiValueDictKeyError:
        address = False
    try:
        speciality = request.GET["speciality"]

    except MultiValueDictKeyError:
        speciality = False
    try:
        phno = request.GET["phno"]

    except MultiValueDictKeyError:
        phno = False
    try:
        sc = request.GET["schedule"]

    except MultiValueDictKeyError:
        sc = False
    p = Doctor.objects.get(Uid=Did)
    # p.name = name
    p.age = age
    # p.gender = gender
    p.address = address
    p.schedule = sc
    p.speciality = speciality
    p.phonenumber = phno
    p.save()
    messages.success(request, 'Profile updated successfully')
    return render(request, 'Doctor.html')

# def updateChemist(request):
#     current_user = request.user

#     Uid = current_user.Uid
#     # print(current_user)
#     # print(Did)

#     # try:
#     #     name = request.GET["name"]

#     # except MultiValueDictKeyError:
#     #     name = False

#     try:
#         age = request.GET["age"]

#     except MultiValueDictKeyError:
#         age = False
#     try:
#         phonenumber = request.GET["phonenumber"]
#     except MultiValueDictKeyError:
#         phonenumber = False
#     try:
#         gender = request.GET["gender"]

#     except MultiValueDictKeyError:
#         gender = False

#     c = Chemist.objects.get(Uid=Uid)
#     # p.name = name
#     c.age = age
#     # p.gender = gender
#     c.phonenumber = phonenumber
#     c.gender = gender
#     # p.speciality = speciality
#     # p.phonenumber = phno
#     c.save()
#     messages.success(request, 'Profile updated successfully')
#     context = {'form' : form}
#     return render(request, 'Chemist.html', context)


# pateint history
def patientHistory(request):
    my_history = None
    pat = None
    if request.user.patient == True:
        p = Patient.objects.get(Uid=request.user.Uid)
        my_history = PatientHistory.objects.filter(Pid=p)

        pat = Patient.objects.get(Uid=request.user.Uid)
    else:
        id = request.POST["patient"]
        print(id)
        p = Patient.objects.get(Uid=id)
        my_history = PatientHistory.objects.filter(Pid=p)
        pat = Patient.objects.filter(Uid=id).first()

    # print(request.user.id)
    print(pat.name)
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
