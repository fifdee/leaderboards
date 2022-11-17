from django.urls import path

from leaderboards.views import LeaderboardList, LeaderboardDetail, LeaderboardCreate, LeaderboardUpdate, \
    LeaderboardDelete, ScoreAdd

urlpatterns = [
    path('', LeaderboardList.as_view(), name='leaderboard-list'),
    path('detail/<int:pk>/', LeaderboardDetail.as_view(), name='leaderboard-detail'),
    path('create/', LeaderboardCreate.as_view(), name='leaderboard-create'),
    path('update/<int:pk>/', LeaderboardUpdate.as_view(), name='leaderboard-update'),
    path('delete/<int:pk>/', LeaderboardDelete.as_view(), name='leaderboard-delete'),
    path('scores/add/', ScoreAdd.as_view(), name='score-add'),
]