"""API_Surveys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin

from FABRIQUE_POLLS.views.admin import AdminPolls, Adminpoll_id, AdminQuestions, AdminQuestionId
from FABRIQUE_POLLS.views.user import Polls, PollById, PollsByUser

urlpatterns = [
    path('polls', Polls.as_view()),
    path('admin1/', admin.site.urls),
    path('polls/<int:id>', PollById.as_view()),
    path('pollsByUser/<int:id>', PollsByUser.as_view()),
    path('admin/', include([
        path('polls', AdminPolls.as_view()),
        path('polls/<int:id>', Adminpoll_id.as_view()),
        path('polls/<int:id>/questions', AdminQuestions.as_view()),
        path('polls/<int:poll_id>/questions/<int:questionId>', AdminQuestionId.as_view())
    ]))
]