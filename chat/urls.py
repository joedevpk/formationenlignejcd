from django.urls import path
from . import views
from .views import upload_file

urlpatterns = [
    path('', views.conversations, name='chat_list'),
    path('<int:user_id>/', views.chat_view, name='chat'),
    path("upload/<int:user_id>/", views.upload_file, name="upload_file")
]

