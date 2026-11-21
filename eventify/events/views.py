from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event, Category

def home(request):
    return render(request, "home.html", {"events": Event.objects.filter(status="upcoming")[:6], "categories": Category.objects.all()})

def event_list(request):
    qs = Event.objects.select_related("category")
    q, cat = request.GET.get("q", ""), request.GET.get("category", "")
    if q: qs = qs.filter(title__icontains=q) | qs.filter(venue__icontains=q)
    if cat: qs = qs.filter(category_id=cat)
    page = Paginator(qs, 6).get_page(request.GET.get("page"))
    return render(request, "events/list.html", {"page": page, "categories": Category.objects.all(), "q": q, "cat": cat})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg = request.user.is_authenticated and event.registrations.filter(user=request.user).first()
    return render(request, "events/detail.html", {"event": event, "reg": reg})

def _check_owner(user, event):
    if not (user.is_staff or event.organizer_id == user.id): raise PermissionDenied

@login_required
def event_create(request):
    if not request.user.profile.can_organize(): raise PermissionDenied
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        ev = form.save(commit=False); ev.organizer = request.user; ev.save()
        messages.success(request, "Event created."); return redirect("event_detail", pk=ev.pk)
    return render(request, "events/form.html", {"form": form, "title": "Create Event"})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk); _check_owner(request.user, event)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Event updated."); return redirect("event_detail", pk=pk)
    return render(request, "events/form.html", {"form": form, "title": "Edit Event"})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk); _check_owner(request.user, event)
    if request.method == "POST":
        event.delete(); messages.success(request, "Event deleted."); return redirect("dashboard")
    return render(request, "events/confirm_delete.html", {"event": event})
