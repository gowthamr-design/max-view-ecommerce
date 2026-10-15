from .cart import SessionCart


def cart_processor(request):
    """Provides cart state to all templates globally."""
    cart = SessionCart(request)
    return {
        'cart': cart,
        'cart_item_count': len(cart),
        'cart_subtotal': cart.get_subtotal(),
        'cart_shipping': cart.get_shipping_cost(),
        'cart_grand_total': cart.get_grand_total(),
    }
