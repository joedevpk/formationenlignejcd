from django.urls import path
from . import views  # importer les vues de courses/views.py

#  URL patterns pour l'app 'courses'
urlpatterns = [
    #  page d'accueil des cours
    path('', views.home, name='home'),

    #  page détail d'un cours
    # <int:id> → on récupère l'ID du cours dans la vue
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('instructor/add-course/', views.add_course, name='add_course'),

    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    
]