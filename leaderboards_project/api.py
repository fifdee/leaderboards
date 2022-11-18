from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from leaderboards.models import Score, Leaderboard
from leaderboards_project.utils import get_random_id

api = NinjaAPI()


class ScoreIn(Schema):
    leaderboard_private_key: str
    player_name: str
    points: int


@api.post('/scores/add')
def hello(request, data: ScoreIn):
    if not request.session.get('player_id'):
        print('randomizing new player_id')
        request.session['player_id'] = get_random_id()

    print(f'player_id: {request.session["player_id"]}')
    print(f'leaderboard_private_key: {data.leaderboard_private_key}')
    print(f'player_name: {data.player_name}')
    print(f'points: {data.points}')

    leaderboard = get_object_or_404(Leaderboard, private_key=data.leaderboard_private_key)

    score = Score.objects.filter(player_id=request.session["player_id"])[0]
    if score:
        if score.points < data.points:
            score.points = data.points
            score.save()
            return f'Score has been updated.'
        else:
            return f'Previous score was higher.'
    else:
        Score.objects.create(
            leaderboard=leaderboard,
            player_id=request.session["player_id"],
            name=data.player_name,
            points=data.points
        )
        return f'Score has been submitted.'

