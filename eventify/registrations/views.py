import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from events.models import Event
from .models import Registration

@login_required
@require_POST
def register(request, pk):
    with transaction.atomic():  # lock the event row so two users can't take the last seat
        event = Event.objects.select_for_update().get(pk=pk)
        reg = Registration.objects.filter(user=request.user, event=event).first()
        if reg and reg.status in ("pending", "confirmed"):
            messages.warning(request, "You are already registered for this event.")
        elif reg and reg.status == "rejected":
            messages.error(request, "Your registration was rejected by the organizer.")
        elif not event.is_open:
            messages.error(request, "Registration is closed (deadline passed, event full or not open).")
        else:
            if reg: reg.status = "pending"; reg.save()
            else: reg = Registration.objects.create(user=request.user, event=event)
            messages.success(request, f"Registered! Your registration ID is {reg.reg_id} (status: Pending).")
    return redirect("event_detail", pk=pk)

@login_required
@require_POST
def cancel(request, pk):
    reg = get_object_or_404(Registration, pk=pk, user=request.user)
    if reg.status in ("pending", "confirmed"):
        reg.status = "cancelled"; reg.save(); messages.success(request, "Registration cancelled. Your seat was released.")
    return redirect("my_registrations")

@login_required
def my_registrations(request):
    return render(request, "registrations/mine.html", {"regs": request.user.registrations.select_related("event")})

def _manageable(user):
    qs = Registration.objects.select_related("user", "event")
    if user.is_staff: return qs
    if user.profile.can_organize(): return qs.filter(event__organizer=user)
    raise PermissionDenied

@login_required
def manage(request):
    qs = _manageable(request.user)
    if request.GET.get("event"): qs = qs.filter(event_id=request.GET["event"])
    if request.GET.get("export") == "csv":  # registration report
        r = HttpResponse(content_type="text/csv"); r["Content-Disposition"] = "attachment; filename=registrations.csv"
        w = csv.writer(r); w.writerow(["Reg ID", "User", "Email", "Event", "Status", "Date"])
        for x in qs: w.writerow([x.reg_id, x.user.username, x.user.email, x.event.title, x.status, x.created_at.date()])
        return r
    return render(request, "registrations/manage.html", {"regs": qs})

@login_required
@require_POST
def set_status(request, pk, action):
    reg = get_object_or_404(_manageable(request.user), pk=pk)
    if action in ("confirmed", "rejected"):
        if action == "confirmed" and reg.status in ("rejected", "cancelled") and not reg.event.available_seats:
            messages.error(request, "No seats left.")
        else:
            reg.status = action; reg.save(); messages.success(request, f"{reg.reg_id} marked {action}.")
    return redirect("manage_registrations")
