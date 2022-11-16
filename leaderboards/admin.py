from django.contrib import admin

from leaderboards.models import User, Leaderboard, Score

# Register your models here.
admin.site.register(User)
admin.site.register(Leaderboard)
admin.site.register(Score)