from django.utils import timezone
from django.forms import PasswordInput
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import (
    User,
    Form,
    Transaction,
    Patient,
    Doctor,
    HCAdmin,
    Medicine,
    FormMedicine,
    Accounts,
    FormTest,
    Test,
)
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .utils import (
    MAKE_PASSWORD,
    CHECK_PASSWORD,
    IsLoggedIn,
)

# Create your views here.
from django.http import HttpResponse


def login(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signin.html")
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")
        elif user.roles == "hcadmin":
            return HttpResponseRedirect("/user/hcadmin_dashboard")
        elif user.roles == "doctor":
            return HttpResponseRedirect("/user/doctor_dashboard")
        elif user.roles == "accounts":
            return HttpResponseRedirect("/user/accounts_dashboard")
        else:
            messages.error(request, "Invalid user")
            return HttpResponseRedirect("/user")


def patientsignup(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request, "signup.html")
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")


def registerPatient(request):
    user = IsLoggedIn(request)
    if user is None:
        if request.method == "POST":
            name = request.POST.get("name")
            username = request.POST.get("username")
            roll = request.POST.get("roll")
            email = request.POST.get("email")
            designation = request.POST.get("designation")
            department = request.POST.get("department")
            password = MAKE_PASSWORD(request.POST.get("password"))
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already in use!")
                return HttpResponseRedirect("/user/signup")
            else:
                user = User(roles="patient")
                user.name = name
                user.username = username
                user.roll = roll
                user.email = email
                user.password = password
                user.designation = designation
                user.save()
                patient = Patient(user=user, department=department)
                patient.save()

                messages.success(request, "User account created successfully!")
                return HttpResponseRedirect("/user")
    else:
        return HttpResponseRedirect("/user/patient_dashboard")


def loginUser(request):
    user = IsLoggedIn(request)
    if user is None:  # user is not already login
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if CHECK_PASSWORD(password, user.password):
                    request.session["username"] = username
                    request.session.modified = True
                    # based on roles render pages
                    if user.roles == "patient":
                        return HttpResponseRedirect("/user/patient_dashboard")
                    elif user.roles == "hcadmin":
                        return HttpResponseRedirect("/user/hcadmin_dashboard")
                    elif user.roles == "doctor":
                        return HttpResponseRedirect("/user/doctor_dashboard")
                    elif user.roles == "accounts":
                        return HttpResponseRedirect("/user/accounts_dashboard")
                    else:
                        messages.error(request, "Invalid user")
                        return HttpResponseRedirect("/user")
                else:
                    messages.error(request, "Wrong username or password!")
                    return HttpResponseRedirect(
                        "/user"
                    )  # redirect to login(wrong_password)
            else:
                messages.error(request, "User does not exist!")
                return HttpResponseRedirect(
                    "/user"
                )  # redirect to login(user_not_exists)
    else:
        if user.roles == "patient":
            return HttpResponseRedirect("/user/patient_dashboard")
        elif user.roles == "hcadmin":
            return HttpResponseRedirect("/user/hcadmin_dashboard")
        elif user.roles == "doctor":
            return HttpResponseRedirect("/user/doctor_dashboard")
        elif user.roles == "accounts":
            return HttpResponseRedirect("/user/accounts_dashboard")
        else:
            messages.error(request, "Invalid user")
            return HttpResponseRedirect("/user")


def logout(request):
    if request.method == "GET":
        if IsLoggedIn(request) is not None:
            del request.session["username"]
            return HttpResponseRedirect("/user")
        else:
            return HttpResponseRedirect("/user")


def patient(request):
    return render(
        request,
        "patient_dashboard.html",
        {
            "user": IsLoggedIn(request),
            "patient": Patient.objects.get(user=IsLoggedIn(request)),
        },
    )


def form(request):
    user = IsLoggedIn(request)
    if user is not None:
        return render(
            request,
            "form.html",
            {
                "user": IsLoggedIn(request),
                "patient": Patient.objects.get(user=IsLoggedIn(request)),
                "doctors": Doctor.objects.all(),
                "tests": Test.objects.all(),
                "medicines": Medicine.objects.all(),
            },
        )
    else:
        messages.warning(request, "Please login first to fill reimbursement form!")
        return HttpResponseRedirect("/user")


def submitForm(request):
    if request.method == "POST":
        user = IsLoggedIn(request)
        if IsLoggedIn(request) is not None:
            form = Form()
            form.user = user
            # form.userid=user.username
            form.name = request.POST.get("name")
            form.department = request.POST.get("department")
            form.designation = request.POST.get("designation")
            # if form.is_valid():
            #     form_application=form.save(commit=False)
            form.save()
            transaction = Transaction(
                status="Form submitted", form=form, user=user, feedback=""
            )
            # user feedback
            transaction.save()
            return HttpResponse("form submitted" + str(form))
            # return redirect('form_detail', pk=form.pk)
        else:
            messages.warning(request, "Please login first to fill reimbursement form!")
            return HttpResponseRedirect("/user")


def doctor_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"doctor": None, "items": []}
    for d in Doctor.objects.all():
        if d.user == user:
            data["doctor"] = d
            break
    for t in Transaction.objects.all():
        if t.form.hc_medical_advisor == user:
            data["items"].append(
                {
                    "transaction": t,
                    "medicines": FormMedicine.objects.filter(form=t.form),
                    "tests": FormTest.objects.filter(form=t.form),
                }
            )

    return render(request, "doctor_dashboard.html", data)


# displaying dashboards
def patient_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"patient": None, "items": []}
    for p in Patient.objects.all():
        if p.user == user:
            data["patient"] = p
            break
    for t in Transaction.objects.all():
        if t.form.patient.user == user:
            data["items"].append(
                {
                    "transaction": t,
                    "medicines": FormMedicine.objects.filter(form=t.form),
                    "tests": FormTest.objects.filter(form=t.form),
                }
            )

    return render(request, "patient_dashboard.html", data)


def hcadmin_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"hcadmin": None, "items": []}
    for hc in HCAdmin.objects.all():
        if hc.user == user:
            data["hcadmin"] = hc
            break
    for t in Transaction.objects.all():
        data["items"].append(
            {
                "transaction": t,
                "medicines": FormMedicine.objects.filter(form=t.form),
                "tests": FormTest.objects.filter(form=t.form),
            }
        )

    return render(request, "hcadmin_dashboard.html", data)


def accounts_dashboard_display(request):
    user = IsLoggedIn(request)
    data = {"accounts": None, "items": []}
    for acc in Accounts.objects.all():
        if acc.user == user:
            data["accounts"] = acc
            break
    for t in Transaction.objects.all():
        data["items"].append(
            {
                "transaction": t,
                "medicines": FormMedicine.objects.filter(form=t.form),
                "tests": FormTest.objects.filter(form=t.form),
            }
        )
    return render(request, "accounts_dashboard.html", data)


def acceptForDoctorApproval(request, t_no):
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Waiting for Doctor Approval"
        # transaction.save()
        return HttpResponse(
            "you are viewing transaction no "
            + str(t_no)
            + " : "
            + str(transaction.status)
            + " : "
            + str(transaction.form.user.user.username)
        )
    else:
        return HttpResponse("Something is wrong")


# accept, reject and view form logic
def viewRequest(request):
    pass


def acceptFormByHC(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Sent to Accounts"
        # update corresponding feedback
        transaction.account_sent_date = timezone.now()
        # transaction.save() #change it to save and redirect to hcadmin_dashboard
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def rejectFormByHC(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected"
        # update corresponding feedback
        # transaction.save() #change it to save and redirect to hcadmin_dashboard
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def acceptByDoctor(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Waiting HC Admin approval"
        # update corresponding feedback
        transaction.doctor_update_date = timezone.now()
        # transaction.save()
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def rejectByDoctor(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected"
        # update corresponding feedback
        # transaction.save() #change it to save and redirect to hcadmin_dashboard
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def acceptByAccounts(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Approved by Accounts"
        # update corresponding feedback
        transaction.account_approve_date = timezone.now()
        # transaction.save()
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def rejectByAccounts(request):
    t_no = request.POST.get("t_no")
    if Transaction.objects.filter(transaction_id=t_no).exists():
        transaction = Transaction.objects.get(transaction_id=t_no)
        transaction.status = "Rejected"
        # update corresponding feedback
        # transaction.save()
        return HttpResponse( "you are viewing transaction no " + str(t_no) + " : " + str(transaction.status) + " : " + str(transaction.form.patient.user.username) )
    else:
        return HttpResponse("Something is wrong")


def viewForm(request):
    pass

def viewProfile(request):
    pass
