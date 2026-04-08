def global_context(request):
    return {
        'qr_site': request.build_absolute_uri('/'),
        'qr_whatsapp': 'https://wa.me/243816172056',
        'qr_tiktok': 'https://www.tiktok.com/@tonprofil'
    }
