from django.urls import path

from leaderboards.views import LeaderboardList, LeaderboardDetail, LeaderboardCreate, LeaderboardUpdate, \
    LeaderboardDelete, ScoreList, ScoreAdd, ScoreDelete, FeedbackSend, FeedbackSendSuccess, ScoresInLeaderboardDetails

urlpatterns = [
    path('', LeaderboardList.as_view(), name='leaderboard-list'),
    path('detail/<int:pk>/', LeaderboardDetail.as_view(), name='leaderboard-detail'),
    path('create/', LeaderboardCreate.as_view(), name='leaderboard-create'),
    path('update/<int:pk>/', LeaderboardUpdate.as_view(), name='leaderboard-update'),
    path('delete/<int:pk>/', LeaderboardDelete.as_view(), name='leaderboard-delete'),
    path('scores/<str:public_key>/', ScoreList.as_view(), name='score-list'),
    path('detail/<int:leaderboard_pk>/', ScoresInLeaderboardDetails.as_view(), name='scores-in-leaderboard-details'),
    path('scores/add/<str:private_key>/', ScoreAdd.as_view(), name='score-add'),
    path('scores/delete/<int:pk>/', ScoreDelete.as_view(), name='score-delete-by-hand'),
    path('contact/', FeedbackSend.as_view(), name='contact'),
    path('contact-success/', FeedbackSendSuccess.as_view(), name='contact-success'),
]