from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone
from events.models import Event, Category
from registrations.models import Registration

@login_required
def dashboard(request):
    u = request.user; ctx = {}
    if u.is_staff or u.profile.role == "organizer":
        events = Event.objects.all() if u.is_staff else Event.objects.filter(organizer=u)
        regs = Registration.objects.filter(event__in=events)
        monthly = regs.annotate(m=TruncMonth("created_at")).values("m").annotate(n=Count("id")).order_by("m")
        cats = Category.objects.filter(events__in=events).annotate(n=Count("events")).values_list("name", "n")
        pop = events.annotate(n=Count("registrations")).order_by("-n")[:5]
        ctx = {"mode": "admin" if u.is_staff else "organizer", "events": events.select_related("category"),
               "total_events": events.count(), "total_regs": regs.count(),
               "upcoming": events.filter(date__gte=timezone.localdate()).count(),
               "recent": regs.select_related("user", "event")[:6],
               "chart": {"cats": list(cats), "months": [[x["m"].strftime("%b %Y"), x["n"]] for x in monthly],
                         "pop": [[e.title, e.n] for e in pop]}}
        if u.is_staff:
            ctx.update(total_users=User.objects.filter(profile__role="participant").count(),
                       total_orgs=User.objects.filter(profile__role="organizer").count())
    else:
        ctx = {"mode": "participant", "regs": u.registrations.select_related("event")[:5]}
    return render(request, "dashboard/dashboard.html", ctx)

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    return render(request, "dashboard/users.html", {"users": User.objects.select_related("profile").order_by("-date_joined")})
