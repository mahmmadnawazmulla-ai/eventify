from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class BootstrapMixin:
    """Adds Bootstrap classes to every field."""
    def style(self):
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "form-select" if isinstance(f.widget, forms.Select) else "form-control")

class SignUpForm(BootstrapMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLES)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.style()
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("This email is already registered.")
        return self.cleaned_data["email"]
    def save(self, commit=True):
        user = super().save(commit=False); user.email = self.cleaned_data["email"]; user.save()
        Profile.objects.filter(user=user).update(role=self.cleaned_data["role"])
        return user

class ProfileForm(BootstrapMixin, forms.ModelForm):
    first_name = forms.CharField(required=False); last_name = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = ["phone", "college"]
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.style()
        u = self.instance.user
        self.fields["first_name"].initial, self.fields["last_name"].initial = u.first_name, u.last_name
    def save(self, commit=True):
        p = super().save(commit)
        p.user.first_name, p.user.last_name = self.cleaned_data["first_name"], self.cleaned_data["last_name"]
        p.user.save(); return p
