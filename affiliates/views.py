from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Affiliate, Commission, Withdrawal
from django.contrib import messages
from .models import Affiliate
import uuid


@login_required
def dashboard(request):

    #  éviter crash
    affiliate, created = Affiliate.objects.get_or_create(user=request.user)

    #  créer code si inexistant
    if not affiliate.code:
        affiliate.code = str(uuid.uuid4())[:8]
        affiliate.save()

    #  importante ici aussi
    commissions = Commission.objects.filter(affiliate=request.user)

    link = f"http://127.0.0.1:8000/?ref={affiliate.code}"

    return render(request, 'affiliates/dashboard.html', {
        'affiliate': affiliate,
        'commissions': commissions,
        'link': link
    })


def leaderboard(request):
    leaders = Commission.objects.values('affiliate__username')\
        .annotate(total=Sum('amount'))\
        .order_by('-total')[:10]

    return render(request, 'affiliates/leaderboard.html', {
        'leaders': leaders
    })


# affiliates/views.py
@login_required
def withdraw(request):
    # Récupérer ou créer l'affiliation pour l'utilisateur actuel
    affiliate, created = Affiliate.objects.get_or_create(user=request.user)

    if created:
        messages.info(request, "Ton compte d'affiliation a été créé automatiquement.")

    if request.method == "POST":
        phone = request.POST.get('phone')
        # On retire tout le solde (ou tu peux modifier pour retirer un montant spécifique)
        if affiliate.balance > 0:
            amount = affiliate.balance
            affiliate.balance = 0
            affiliate.save()
            messages.success(request, f"Retrait de {amount}$ effectué avec succès !")
        else:
            messages.error(request, "Votre solde est nul, rien à retirer.")
        return redirect('withdraw')

    context = {
        'affiliate': affiliate
    }
    return render(request, 'affiliates/withdraw.html', context)