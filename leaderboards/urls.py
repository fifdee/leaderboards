from django.urls import path

from leaderboards.views import LeaderboardList, LeaderboardDetail, LeaderboardCreate, LeaderboardUpdate, \
    LeaderboardDelete

urlpatterns = [
    path('', LeaderboardList.as_view(), name='leaderboard-list'),
    path('', LeaderboardDetail.as_view(), name='leaderboard-detail'),
    path('', LeaderboardCreate.as_view(), name='leaderboard-create'),
    path('', LeaderboardUpdate.as_view(), name='leaderboard-update'),
    path('', LeaderboardDelete.as_view(), name='leaderboard-delete'),
]