from django.forms import ModelForm

from leaderboards.models import Leaderboard


class LeaderboardForm(ModelForm):
    class Meta:
        model = Leaderboard
        fields = ['name']