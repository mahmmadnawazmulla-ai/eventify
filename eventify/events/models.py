from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name_plural = "categories"
    def __str__(self): return self.name

class Event(models.Model):
    STATUS = [("upcoming", "Upcoming"), ("ongoing", "Ongoing"), ("completed", "Completed"), ("cancelled", "Cancelled")]
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    image = models.ImageField(upload_to="events/", blank=True)
    date = models.DateField(); start_time = models.TimeField(); end_time = models.TimeField()
    venue = models.CharField(max_length=150)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    max_participants = models.PositiveIntegerField()
    registration_deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default="upcoming")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["date", "start_time"]
    def __str__(self): return self.title
    @property
    def seats_taken(self):  # pending + confirmed registrations hold a seat
        return self.registrations.filter(status__in=["pending", "confirmed"]).count()
    @property
    def available_seats(self): return max(self.max_participants - self.seats_taken, 0)
    @property
    def is_open(self):
        return self.status == "upcoming" and timezone.localdate() <= self.registration_deadline and self.available_seats > 0
