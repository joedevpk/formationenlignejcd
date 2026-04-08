from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
import base64
from .models import Plan, Subscription
from courses.models import Course
from .utils import generate_qr_code
from notifications.utils import send_notification
from affiliates.utils import give_commission  #



@login_required
def plans_view(request):
    plans = Plan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})


@login_required
def subscribe(request, plan_id):
    #  Récupère le plan
    plan = get_object_or_404(Plan, id=plan_id)

    #  Crée ou récupère la subscription pour l'utilisateur
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        plan=plan,
        defaults={
            'amount': plan.price,
            'status': 'pending',
            'is_active': False
        }
    )

    #  Générer le QR code pour le paiement
    qr_base64 = None
    try:
        payment_data = f"Mpesa:+243816172056 | Montant:{plan.price}$"
        qr = generate_qr_code(payment_data)
        qr_base64 = base64.b64encode(qr.getvalue()).decode()
    except Exception as e:
        print("Erreur QR CODE :", e)

    #  Si le formulaire est soumis
    if request.method == "POST":
        proof = request.FILES.get('proof')
        if proof:
            subscription.proof = proof
            subscription.amount = plan.price
            subscription.status = 'pending'
            subscription.is_active = False
            subscription.save()
            
            # Redirige ou affiche page succès
            return render(request, 'subscriptions/subscription_success.html', {
                'plan': plan,
                'subscription': subscription
            })
        else:
            # Formulaire soumis mais sans fichier
            return render(request, 'subscriptions/upload_proof.html', {
                'plan': plan,
                'qr_code': qr_base64,
                'subscription': subscription,
                'error': "Veuillez ajouter une preuve de paiement"
            })

    #  GET : affiche le formulaire avec QR code
    return render(request, 'subscriptions/upload_proof.html', {
        'plan': plan,
        'qr_code': qr_base64,
        'subscription': subscription,
    })


@login_required
def popular_courses(request):
    popular_courses = Course.objects.filter(lessons__is_popular=True).distinct()
    return render(request, 'subscriptions/popular_courses.html', {'popular_courses': popular_courses})


@login_required
def admin_payments_view(request):
    # Récupérer tous les abonnements avec preuve, triés par date desc
    payments = Subscription.objects.filter(proof__isnull=False).order_by('-created_at')
    return render(request, 'subscriptions/admin_payments.html', {'payments': payments})

 

@login_required
@require_POST
def validate_payment(request, payment_id):
    if not getattr(request.user, 'is_finance_admin', False):
        return redirect('dashboard_redirect')

    payment = get_object_or_404(Subscription, id=payment_id)

    if payment.status != 'approved':
        payment.status = 'approved'
        payment.is_active = True

        if not payment.end_date or payment.end_date < timezone.now():
            payment.end_date = timezone.now() + timedelta(days=payment.plan.duration_days)

        payment.save()

        # AJOUT ICI (TRÈS IMPORTANT)
        give_commission(payment.user, payment.plan.price)

    return redirect('admin_payments')



@login_required
@require_POST
def reject_payment(request, payment_id):
    if not getattr(request.user, 'is_finance_admin', False):
        return redirect('dashboard_redirect')

    payment = get_object_or_404(Subscription, id=payment_id)

    if payment.status != 'rejected':
        payment.status = 'rejected'
        payment.is_active = False
        payment.save()

    return redirect('admin_payments')


