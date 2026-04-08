from django.urls import path
#from .views import admin_dashboard
from . import views
from .views import PrivacyView, TermsView, MentionsView, CookiesView

urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
   # path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('help/', views.help_page, name='help'),
    path('contact/', views.contact, name='contact'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),

    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('mentions/', MentionsView.as_view(), name='mentions'),
    path('cookies/', CookiesView.as_view(), name='cookies'),
    
    
]

