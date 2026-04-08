from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from affiliates.models import Affiliate, Referral
from django.contrib import messages



# 🟢 INSCRIPTION

def register_view(request):

    ref_code = request.GET.get('ref') or request.session.get('ref_code')

    if request.GET.get('ref'):
        request.session['ref_code'] = request.GET.get('ref')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            #  AFFILIATION
            if ref_code:
                try:
                    affiliate = Affiliate.objects.get(code=ref_code)

                    if (
                        affiliate.user != user and
                        not affiliate.user.is_staff and
                        not affiliate.user.is_superuser
                    ):
                        Referral.objects.get_or_create(
                            referrer=affiliate.user,
                            referred_user=user
                        )

                        # 
                        messages.success(request, f"🎉 Iscription réussie ✅! Parrain : {affiliate.user.username}")

                except Affiliate.DoesNotExist:
                    messages.error(request, "❌ Code d’affiliation invalide")

            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ message succès
            messages.success(request, "🎉 Connexion réussie ✅ !")

            return redirect('home')
        else:
            # ❌ message erreur
            messages.error(request, "❌ Nom ou mot de passe incorrect")

    return render(request, 'accounts/login.html', {
        'form': form
    })


# 🔴 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')