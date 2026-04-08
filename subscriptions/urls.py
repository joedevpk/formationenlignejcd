from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plans_view, name='plans'),
    path('subscriptions/subscribe/<int:plan_id>/', views.subscribe, name='subscrition_success'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('popular/', views.popular_courses, name='popular_courses'),  # <-- bouton pointe ici
    path('admin/payments/', views.admin_payments_view, name='admin_payments'),
    path('validate/<int:payment_id>/', views.validate_payment, name='validate_payment'),
    path('admin/payments/validate/<int:payment_id>/', views.validate_payment, name='validate_payment'),
    path('admin/payments/reject/<int:payment_id>/', views.reject_payment, name='reject_payment'), 
    path('reject/<int:payment_id>/', views.reject_payment, name='reject_payment'), 
]


