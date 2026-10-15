from apps.core.models import SiteConfig
from apps.catalog.models import Category


def global_settings(request):
    """Provides site config and category hierarchy to all templates."""
    try:
        site_config = SiteConfig.objects.first()
    except Exception:
        site_config = None

    if not site_config:
        site_config = {
            'site_name': 'MAX VIEW',
            'support_email': 'maxview1@gmail.com',
            'support_phone': '1234567890',
            'store_address': '123@ Tirupur, Tamil Nadu, Old Bus Stand Tirupur, INDIA',
            'free_shipping_threshold': 999.00,
        }

    try:
        nav_categories = Category.objects.filter(is_active=True).order_by('display_order')
    except Exception:
        nav_categories = []

    return {
        'site_config': site_config,
        'nav_categories': nav_categories,
    }
