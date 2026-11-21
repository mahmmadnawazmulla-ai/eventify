from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Category, Event

class Command(BaseCommand):
    help = "Create sample categories, users and events"
    def handle(self, *a, **k):
        names = ["Technical Events", "Workshops", "Cultural Events", "Sports Events", "Seminars", "Competitions", "Festivals"]
        cats = [Category.objects.get_or_create(name=n)[0] for n in names]
        org, _ = User.objects.get_or_create(username="organizer1", defaults={"email": "org@example.com"})
        org.set_password("Organizer@123"); org.save(); org.profile.role = "organizer"; org.profile.save()
        u, _ = User.objects.get_or_create(username="student1", defaults={"email": "s1@example.com"})
        u.set_password("Student@123"); u.save()
        today = timezone.localdate()
        for i, c in enumerate(cats):
            Event.objects.get_or_create(title=f"{c.name[:-1] if c.name.endswith('s') else c.name} Meet {i+1}", defaults=dict(
                description="Join us for an exciting event with talks, activities and networking.", category=c,
                date=today + timedelta(days=7 + i * 5), start_time="10:00", end_time="16:00", venue=f"Hall {i+1}, Main Campus",
                organizer=org, max_participants=20 + i * 10, registration_deadline=today + timedelta(days=5 + i * 5)))
        self.stdout.write("Seeded. Logins: organizer1/Organizer@123, student1/Student@123")
