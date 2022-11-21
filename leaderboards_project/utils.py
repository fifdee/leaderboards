from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from leaderboards.models import Leaderboard, Score


def get_random_id():
    import uuid
    return str(uuid.uuid4())


def add_or_update_score(data, is_get_request=False):
    leaderboard = get_object_or_404(Leaderboard, private_key=data.leaderboard_private_key)

    score = None
    try:
        score = Score.objects.get(leaderboard=leaderboard, name=data.name)
    except Exception as e:
        print(e)
    finally:
        if score:
            score.extra = data.extra
            score.save()
            if score.points < data.points:
                score.points = data.points
                score.submitted_date = now()
                score.save()
                if is_get_request:
                    return HttpResponse('Score has been updated.')
                return f'Score has been updated.'
            else:
                if is_get_request:
                    return HttpResponse('Previous score was higher.')
                return f'Previous score was higher.'
        else:
            max_scores_count = 50
            if Score.objects.filter(leaderboard=leaderboard).count() >= max_scores_count:
                Score.objects.filter(leaderboard=leaderboard).order_by('-points').last().delete()

            Score.objects.create(
                leaderboard=leaderboard,
                name=data.name,
                points=data.points,
                submitted_date=now(),
                extra=data.extra
            )
            if is_get_request:
                return HttpResponse('Score has been submitted.')
            return f'Score has been submitted.'
