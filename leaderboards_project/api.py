from datetime import date, datetime
from typing import List

from ninja import NinjaAPI, Schema

from leaderboards.models import Score
from leaderboards_project.utils import add_or_update_score

api = NinjaAPI(urls_namespace='api')


class ScoreIn(Schema):
    leaderboard_private_key: str
    name: str
    points: int
    time: str = ''
    extra: str = ''
    uuid: str = ''


class ScoreOut(Schema):
    name: str
    points: int
    time: str
    extra: str
    uuid: str
    submitted_date: datetime


class ScoreDelete(Schema):
    leaderboard_private_key: str
    uuid: str = ''
    name: str = ''


@api.post('/scores/add')
def score_add(request, data: ScoreIn):
    print(f'leaderboard_private_key: {data.leaderboard_private_key}')
    print(f'name: {data.name}')
    print(f'points: {data.points}')
    print(f'time: {data.time}')
    print(f'extra info: {data.extra}')
    print(f'uuid: {data.uuid}')

    return add_or_update_score(data)


@api.post('/scores/delete')
def score_delete(request, data: ScoreDelete, url_name='score_delete'):
    print('Deleting score')
    print(f'leaderboard_private_key: {data.leaderboard_private_key}')
    print(f'name: {data.name}')
    print(f'uuid: {data.uuid}')

    score = None
    try:
        if data.uuid != '':
            score = Score.objects.get(leaderboard__private_key=data.leaderboard_private_key, uuid=data.uuid)
        else:
            score = Score.objects.get(leaderboard__private_key=data.leaderboard_private_key, name=data.name)
    except Score.MultipleObjectsReturned:
        if data.uuid != '':
            score = Score.objects.filter(leaderboard__private_key=data.leaderboard_private_key, uuid=data.uuid)
        else:
            score = Score.objects.filter(leaderboard__private_key=data.leaderboard_private_key, name=data.name)
    except Score.DoesNotExist:
        return 'Score with provided information does not exist.'
    except Exception as e:
        print(e)
    finally:
        if score:
            score.delete()
            return 'Score has been deleted.'


@api.get('/scores/{public_key}', response=List[ScoreOut], url_name='scores')
def scores(request, public_key: str):
    scores = Score.objects.filter(leaderboard__public_key=public_key).order_by('-points')
    return scores


@api.get('/scores/{public_key}/{name}', response=List[ScoreOut], url_name='user_score')
def user_score(request, public_key: str, name: str):
    score = Score.objects.filter(leaderboard__public_key=public_key, name=name)
    return score


@api.get('/scores/{public_key}/uuid/{uuid}', response=List[ScoreOut], url_name='user_score_uuid')
def user_score(request, public_key: str, uuid: str):
    score = Score.objects.filter(leaderboard__public_key=public_key, uuid=uuid)
    return score
