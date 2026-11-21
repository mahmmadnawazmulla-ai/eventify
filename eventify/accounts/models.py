from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLES = [("participant", "Participant"), ("organizer", "Organizer")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=12, choices=ROLES, default="participant")
    phone = models.CharField(max_length=15, blank=True)
    college = models.CharField(max_length=100, blank=True)
    def can_organize(self):
        return self.role == "organizer" or self.user.is_staff
    def __str__(self):
        return f"{self.user.username} ({self.role})"

@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kw):
    if created:
        Profile.objects.create(user=instance)
