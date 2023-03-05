from allauth.account.forms import SignupForm, ResetPasswordForm
from allauth.account.utils import filter_users_by_email
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


class UserConvertForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]

        user = request.user
        if user.is_authenticated:
            user.email = email
            user.save()

        self.users = filter_users_by_email(email, is_active=True)

        if not self.users:
            self._send_unknown_account_mail(request, email)
        else:
            self._send_password_reset_mail(request, email, self.users, **kwargs)
        return email