import uuid
from django.contrib.auth.models import User
from django.db import models
from events.models import Event

def new_reg_id(): return "REG-" + uuid.uuid4().hex[:8].upper()

class Registration(models.Model):
    STATUS = [("pending", "Pending"), ("confirmed", "Confirmed"), ("rejected", "Rejected"), ("cancelled", "Cancelled")]
    reg_id = models.CharField(max_length=14, unique=True, default=new_reg_id, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "event"], name="one_registration_per_user_event")]
        ordering = ["-created_at"]
    def __str__(self): return f"{self.reg_id} - {self.user} - {self.event}"
