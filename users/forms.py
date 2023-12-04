from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]
        labels = {"first_name": "Name"}
    def __init__(self, *args, **kwargs) -> None:
        super(UserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "username",
            "location",
            "bio",
            "short_intro",
            "profile_image",
            "social_github",
            "social_linkdin",
            "social_youtube",
            "social_twitter",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs) -> None:
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs) -> None:
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
