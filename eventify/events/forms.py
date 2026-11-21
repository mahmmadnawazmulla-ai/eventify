from django import forms
from accounts.forms import BootstrapMixin
from .models import Event

class EventForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["organizer", "created_at"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}), "registration_deadline": forms.DateInput(attrs={"type": "date"}),
                   "start_time": forms.TimeInput(attrs={"type": "time"}), "end_time": forms.TimeInput(attrs={"type": "time"}),
                   "description": forms.Textarea(attrs={"rows": 4})}
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.style()
    def clean(self):
        d = super().clean()
        if d.get("start_time") and d.get("end_time") and d["end_time"] <= d["start_time"]:
            raise forms.ValidationError("End time must be after start time.")
        if d.get("date") and d.get("registration_deadline") and d["registration_deadline"] > d["date"]:
            raise forms.ValidationError("Registration deadline cannot be after the event date.")
        return d
    def clean_max_participants(self):
        n = self.cleaned_data["max_participants"]
        if n < 1: raise forms.ValidationError("Capacity must be at least 1.")
        return n
