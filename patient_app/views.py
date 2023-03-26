from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from dashboard_app.models import *
from .forms import *
import datetime







# ==================================================
#                     DASHBOARD VIEWS
# ==================================================
# DASHBOARD VIEW 
@login_required
def patient_view(request):
    user = request.user
    appointments = Appointment.objects.filter(patient__user=user)
    appointment_count = Appointment.objects.filter(patient__user=user).count()
    symptoms_count = AppointmentPrescription.objects.filter(appointment__patient__user=user).count()
    prescription_count = AppointmentPrescription.objects.filter(appointment__patient__user=user).count()
    context = {
        'appointment_count': appointment_count,
        'symptoms_count': symptoms_count,
        'prescription_count': prescription_count,
        'appointments':appointments,
        'today': datetime.date.today()
    }
    template = "patient/index.html"
    return render(request,template,context)

    



@login_required
def appoitment_view(request):
    user = request.user
    appointments = Appointment.objects.filter(patient__user=user)
    context = {
        'appointments': appointments,
        'today': datetime.date.today()
    }
    template = "patient/appointment.html"
    return render(request,template,context)

    




# APPOINTMENT ADD VIEW 
@login_required
def appointment_add_view(request):
    patient  = get_object_or_404(Patient, user=request.user.id)
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient=patient
            date = form.cleaned_data.get("date")
            hour = form.cleaned_data.get("hour")
            appointment.save()
            subject = "Nouveau rendez-vous le "+str(date)+" à "+str(hour)
            Notification.objects.create(appointment=appointment, subject=subject)
            messages.success(request, _("Rendez-Vous créé avec succès."))
            return redirect('patient:appointment')
    else:
        form = PatientAppointmentForm()
    context = {'form': form}
    template = "patient/appointment-add.html"
    return render(request, template, context)


 



# APPOINTMENT UPDATE VIEW FUNCTION
@login_required
def appointment_update_view(request, id):
    obj  = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Rendez-vous mis à jour avec succès."))
            return redirect('patient:appointment')
    else:
        form = PatientAppointmentForm(instance=obj)
    context = {  'form': form}
    template = "patient/appointment-update.html"
    return render(request, template, context)







@login_required
def symptom_view(request):
    user = request.user
    patient  = get_object_or_404(Patient, user=user)
    symptoms = AppointmentPrescription.objects.filter(appointment__patient=patient)
    context  = {'symptoms': symptoms}
    template = "patient/symptom.html"
    return render(request,template,context)

    





@login_required
def prescription_view(request):
    user = request.user
    patient  = get_object_or_404(Patient, user=user)
    prescriptions = AppointmentPrescription.objects.filter(appointment__patient=patient)
    context = {'prescriptions': prescriptions}
    template = "patient/prescription.html"
    return render(request,template,context)

    











@login_required
def profile_view(request):
    obj  = get_object_or_404(Profile, user=request.user.id)
    if obj.photo:
        profile_photo = obj.photo.url
    else:
        profile_photo = ""
    if request.method == 'POST':
        profile_form = PatientProfileForm(request.POST, request.FILES, instance=obj)
        user_form = PatientUserUpdateForm(request.POST, instance=obj.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile modifié avec succès."))
            return redirect('patient:profile')
    else:
        user_form = PatientUserUpdateForm(instance=obj.user)
        profile_form = PatientProfileForm(instance=obj)
    context  = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_photo': profile_photo
    }
    template = "patient/profile.html"
    return render(request, template, context)

