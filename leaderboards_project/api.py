from datetime import date
from typing import List

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from ninja import NinjaAPI, Schema

from leaderboards.models import Score, Leaderboard
from leaderboards_project.utils import get_random_id

api = NinjaAPI(urls_namespace='api')


class ScoreIn(Schema):
    leaderboard_private_key: str
    player_name: str
    points: int
    extra: str = ''


class ScoreOut(Schema):
    name: str
    points: int
    submitted_date: date


@api.post('/scores/add')
def score_add(request, data: ScoreIn):
    if not request.session.get('player_id'):
        print('randomizing new player_id')
        request.session['player_id'] = get_random_id()

    print(f'player_id: {request.session["player_id"]}')
    print(f'leaderboard_private_key: {data.leaderboard_private_key}')
    print(f'player_name: {data.player_name}')
    print(f'points: {data.points}')
    print(f'extra info: {data.extra}')

    leaderboard = get_object_or_404(Leaderboard, private_key=data.leaderboard_private_key)

    score = None
    try:
        score = Score.objects.get(leaderboard=leaderboard, player_id=request.session["player_id"])
    except Exception as e:
        print(e)

    if score:
        score.name = data.player_name
        score.extra = data.extra
        score.save()
        if score.points < data.points:
            score.points = data.points
            score.submitted_date = now()
            score.save()
            return f'Score has been updated.'
        else:
            return f'Previous score was higher.'
    else:
        max_scores_count = 50
        if Score.objects.filter(leaderboard=leaderboard).count() >= max_scores_count:
            Score.objects.filter(leaderboard=leaderboard).order_by('-points').last().delete()

        Score.objects.create(
            leaderboard=leaderboard,
            player_id=request.session["player_id"],
            name=data.player_name,
            points=data.points,
            submitted_date=now(),
            extra=data.extra
        )
        return f'Score has been submitted.'


@api.get('/scores/{public_key}', response=List[ScoreOut], url_name='scores')
def scores(request, public_key: str):
    scores = Score.objects.filter(leaderboard__public_key=public_key)
    return scores
