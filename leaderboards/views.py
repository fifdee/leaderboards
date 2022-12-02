from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from leaderboards.forms import LeaderboardForm
from leaderboards.models import Leaderboard, Score
from leaderboards_project.utils import get_random_id, add_or_update_score


class Homepage(generic.TemplateView):
    template_name = 'leaderboards/homepage.html'


class LeaderboardList(LoginRequiredMixin, generic.ListView):
    template_name = 'leaderboards/leaderboard_list.html'

    def get_queryset(self):
        return Leaderboard.objects.filter(owner=self.request.user)


class LeaderboardDetail(LoginRequiredMixin, generic.DetailView):
    template_name = 'leaderboards/leaderboard_detail.html'

    def get_queryset(self):
        return Leaderboard.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(LeaderboardDetail, self).get_context_data(**kwargs)
        context['scores'] = Score.objects.filter(leaderboard__owner=self.request.user,
                                                 leaderboard=self.get_object()).order_by('-points')
        context['submit_url'] = self.request.build_absolute_uri(reverse('api:score_add'))
        context['delete_url'] = self.request.build_absolute_uri(reverse('api:score_delete'))

        context['submit_url_get'] = self.request.build_absolute_uri(
            reverse('score-add', kwargs={'private_key': self.get_object().private_key}))

        context['submit_url_get_scheme'] = self.request.build_absolute_uri(
            reverse('score-add', kwargs={'private_key': '(private_key)'}))

        context['retrieve_url'] = self.request.build_absolute_uri(
            reverse('api:scores', kwargs={'public_key': self.get_object().public_key}))

        context['retrieve_url_scheme'] = self.request.build_absolute_uri(
            reverse('api:scores', kwargs={'public_key': '(public_key)'}))

        context['retrieve_url_user'] = self.request.build_absolute_uri(
            reverse('api:user_score', kwargs={'public_key': self.get_object().public_key, 'name': 'John Doe'}))

        context['retrieve_url_user_scheme'] = self.request.build_absolute_uri(
            reverse('api:user_score', kwargs={'public_key': '(public_key)', 'name': '(name)'}))

        context['retrieve_url_user_uuid'] = self.request.build_absolute_uri(
            reverse('api:user_score_uuid',
                    kwargs={'public_key': self.get_object().public_key, 'uuid': 'zxcasdqwe567234'}))

        context['retrieve_url_user_uuid_scheme'] = self.request.build_absolute_uri(
            reverse('api:user_score_uuid', kwargs={'public_key': '(public_key)', 'uuid': '(uuid)'}))

        context['retrieve_url_website'] = self.request.build_absolute_uri(
            reverse('score-list', kwargs={'public_key': self.get_object().public_key}))

        return context


class LeaderboardCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'leaderboards/leaderboard_create.html'
    form_class = LeaderboardForm

    def form_valid(self, form):
        leaderboard = form.save(commit=False)
        leaderboard.owner = self.request.user
        leaderboard.public_key = get_random_id()
        leaderboard.private_key = get_random_id()
        leaderboard.save()

        return redirect('leaderboard-list')


class LeaderboardUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leaderboards/leaderboard_update.html'
    form_class = LeaderboardForm

    def get_queryset(self):
        return Leaderboard.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('leaderboard-list')


class LeaderboardDelete(LoginRequiredMixin, generic.DeleteView):
    template_name = 'leaderboards/leaderboard_delete.html'

    def get_queryset(self):
        return Leaderboard.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('leaderboard-list')


class ScoreList(generic.ListView):
    template_name = 'leaderboards/score_list.html'
    context_object_name = 'scores'

    def get_queryset(self):
        return Score.objects.filter(leaderboard__public_key=self.kwargs['public_key']).order_by('-points')

    def get_context_data(self, *args, **kwargs):
        public_key = self.kwargs['public_key']
        context = super(ScoreList, self).get_context_data(*args, **kwargs)
        context['hide_navbar'] = True
        try:
            context['leaderboard'] = Leaderboard.objects.get(public_key=public_key)
        except Exception as e:
            print(e)

        return context


class ScoreData:
    def __init__(self, leaderboard_private_key, name, points, time, extra, uuid):
        self.leaderboard_private_key = leaderboard_private_key
        self.name = name
        self.points = points
        self.time = time
        self.extra = extra
        self.uuid = uuid


class ScoreAdd(generic.View):
    def get(self, request, private_key):
        name = request.GET.get("name", None)
        points = request.GET.get("points", None)
        time = request.GET.get("time", '')
        extra = request.GET.get("extra", '')
        uuid = request.GET.get("uuid", '')

        print(f'leaderboard_private_key: {private_key}')
        print(f'name: {name}')
        print(f'points: {points}')
        print(f'time: {time}')
        print(f'extra: {extra}')
        print(f'uuid: {uuid}')

        if not name:
            return HttpResponse('Name was not provided.')
        if not points:
            return HttpResponse('Points were not provided.')

        data = ScoreData(private_key, name, int(points), time, extra, uuid)

        return add_or_update_score(data, is_get_request=True)


class ScoreDelete(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        score = get_object_or_404(Score, pk=pk)
        leaderboard_pk = score.leaderboard.pk
        score.delete()
        return redirect('leaderboard-detail', pk=leaderboard_pk)