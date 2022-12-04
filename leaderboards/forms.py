from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm, Form

from leaderboards.models import Leaderboard, Feedback


class LeaderboardForm(ModelForm):
    class Meta:
        model = Leaderboard
        fields = ['name']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'message']
