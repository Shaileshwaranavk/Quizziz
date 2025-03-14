from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='Register_Page'),
    path('login/', views.login_Page, name='login_Page'),
    path('login/quiz/', views.quiz_view, name='quiz'),
    path('login/quiz/check-answer/', views.check_answer, name="check_answer"),
    path('login/leaderboard/', views.leaderboard, name='leaderboard')
]
