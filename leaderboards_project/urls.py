"""leaderboards_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .api import api
from leaderboards.views import Homepage, create_temporary_user, SetEmailResetPassword, score_delete

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('user-create/', create_temporary_user, name='temp-user-create'),
    # path('scores/delete-via-list/', score_delete, name='score-delete-by-hand'),
    path('signup/', SetEmailResetPassword.as_view(), name='signup'),
    path('leaderboards/', include('leaderboards.urls')),
]
