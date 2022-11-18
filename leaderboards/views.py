from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from leaderboards.forms import LeaderboardForm
from leaderboards.models import Leaderboard, Score
from leaderboards_project.utils import get_random_id


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
        return Score.objects.filter(leaderboard__public_key=self.kwargs['public_key'])

    def get_context_data(self, *args, **kwargs):
        context = super(ScoreList, self).get_context_data(*args, **kwargs)
        context['hide_navbar'] = True
        try:
            context['leaderboard'] = Leaderboard.objects.get(public_key=self.kwargs['public_key'])
        except Exception as e:
            print(e)
        return context
