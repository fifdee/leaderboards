from django.shortcuts import render
from django.views import generic


class Homepage(generic.TemplateView):
    template_name = 'leaderboards/homepage.html'


class LeaderboardList(generic.ListView):
    pass


class LeaderboardDetail(generic.DetailView):
    pass


class LeaderboardCreate(generic.CreateView):
    pass


class LeaderboardUpdate(generic.UpdateView):
    pass


class LeaderboardDelete(generic.DeleteView):
    pass
