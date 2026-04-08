from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='affiliate_dashboard'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]