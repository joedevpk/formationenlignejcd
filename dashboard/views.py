from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # pour afficher un message de confirmation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from subscriptions.models import Subscription
from courses.models import Course
from django.views.generic import TemplateView



def finance_dashboard(request):

    #  TOTAL REVENUS VALIDÉS
    total_revenue = Subscription.objects.filter(
        status='approved'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 👥 utilisateurs actifs
    active_users = Subscription.objects.filter(
        status='approved',
        is_active=True
    ).count()

    return render(request, 'dashboard/finance_dashboard.html', {
        'total_revenue': total_revenue,
        'active_users': active_users,

        # mets des valeurs fixes si tu veux tester
        'revenue_percent': 80,
        'revenue_growth': 20,
        'users_percent': 70,
        'users_growth': 15,
        'total_courses': 10,
        'courses_percent': 60,
        'courses_growth': 10,
        'months': [],
        'subscriptions_data': [],
        'revenue_data': []
    })


#  Redirection selon type utilisateur
@login_required
def dashboard_redirect(request):
    """
    Redirige automatiquement l'utilisateur vers son dashboard :
    - admin → admin_dashboard
    - formateur → instructor_dashboard
    - étudiant → student_dashboard
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')
    elif getattr(request.user, 'is_instructor', False):
        return redirect('instructor_dashboard')
    else:
        return redirect('student_dashboard')


#  DASHBOARD FORMATEUR
@login_required
def instructor_dashboard(request):
    """
    Vue du dashboard formateur :
    - liste de ses cours
    - nombre total de cours
    """
    courses = Course.objects.filter(instructor=request.user)
    context = {
        'courses': courses,
        'total_courses': courses.count()
    }
    #if not request.user.is_superuser:
    #return redirect('dashboard_redirect')
    return render(request, 'dashboard/instructor_dashboard.html', context)


#  DASHBOARD ÉTUDIANT
@login_required
def student_dashboard(request):

    #  prendre abonnement VALIDÉ seulement
    subscription = Subscription.objects.filter(
        user=request.user,
        status='approved'
    ).order_by('-end_date').first()

    #  vérifier expiration
    if subscription:
        if subscription.end_date < timezone.now():
            subscription.is_active = False
            subscription.save()

            # email
            send_mail(
                subject="🔔 Votre abonnement est expiré",
                message=f"Bonjour {request.user.username}, votre abonnement a expiré.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True
            )

    #  accès cours seulement si actif
    if subscription and subscription.is_active:
        courses = Course.objects.all()
    else:
        courses = []

    # populaires
    popular_courses = Course.objects.all().order_by('-created_at')[:4]

    return render(request, 'dashboard/student_dashboard.html', {
        'subscription': subscription,
        'courses': courses,
        'popular_courses': popular_courses,
    })



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"Nouveau message de {name}"
        body = f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                ['joedevpk@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Votre message a été envoyé avec succès ! ✅")
            return redirect('contact')
        except Exception as e:
            messages.error(request, "Erreur lors de l'envoi. Veuillez réessayer.")
            print(e)
    
    return render(request, "dashboard/contact.html")


def help_page(request):
    return render(request, "dashboard/help.html")



class PrivacyView(TemplateView):
    template_name = "legal/privacy.html"

class TermsView(TemplateView):
    template_name = "legal/terms.html"

class MentionsView(TemplateView):
    template_name = "legal/mentions.html"

class CookiesView(TemplateView):
    template_name = "legal/cookies.html"