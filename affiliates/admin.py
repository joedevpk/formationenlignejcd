from django.contrib import admin
from .models import Affiliate, Referral, Commission, Withdrawal

admin.site.register(Affiliate)
admin.site.register(Referral)
admin.site.register(Commission)
admin.site.register(Withdrawal)