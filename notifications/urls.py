from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('unread-count/', views.unread_count, name='unread_count'),
    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),

    path('read/<int:notif_id>/', views.mark_one_read, name='mark_one_read'),
    path('delete/<int:notif_id>/', views.delete_notification, name='delete_notification'),
]