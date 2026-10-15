from decimal import Decimal
from django.conf import settings
from apps.catalog.models import Product
from apps.cart.models import Cart, CartItem


class SessionCart:
    """
    Manages session-based shopping cart for both anonymous and authenticated users.
    Enforces server-side price validation by querying active Product records.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.request = request

    def add(self, product, quantity=1, override_quantity=False):
        """Add product to cart or increment quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = max(1, int(quantity))
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        # Cap at available stock
        if self.cart[product_id]['quantity'] > product.stock_quantity:
            self.cart[product_id]['quantity'] = product.stock_quantity

        self.save()

    def update(self, product, quantity):
        """Update specific product quantity."""
        product_id = str(product.id)
        if product_id in self.cart:
            qty = int(quantity)
            if qty <= 0:
                self.remove(product)
            else:
                self.cart[product_id]['quantity'] = min(qty, product.stock_quantity)
                self.save()

    def remove(self, product):
        """Remove product from cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Empty the cart."""
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        """Marks the session as modified to ensure it gets saved."""
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and query database to fetch live products.
        Ensures client prices are never trusted.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True).select_related('category')
        product_map = {str(p.id): p for p in products}

        # Clean up products that might have been deactivated or deleted
        active_cart = {}
        for product_id, item in self.cart.items():
            product = product_map.get(product_id)
            if product:
                item_copy = item.copy()
                item_copy['product'] = product
                item_copy['price'] = product.price
                item_copy['total_price'] = product.price * item_copy['quantity']
                active_cart[product_id] = item
                yield item_copy

        if len(active_cart) != len(self.cart):
            self.cart = active_cart
            self.save()

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        """Calculate real-time subtotal against database prices."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        price_map = {str(p.id): p.price for p in products}

        subtotal = Decimal('0.00')
        for product_id, item in self.cart.items():
            price = price_map.get(product_id, Decimal('0.00'))
            subtotal += price * item['quantity']
        return subtotal

    def get_shipping_cost(self):
        """Free shipping above threshold (₹999), otherwise standard ₹99."""
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal >= Decimal('999.00'):
            return Decimal('0.00')
        return Decimal('99.00')

    def get_grand_total(self):
        """Grand total = subtotal + shipping."""
        return self.get_subtotal() + self.get_shipping_cost()

    def sync_to_database(self, user):
        """Merge current session items into the authenticated user's MySQL Cart."""
        if not user or not user.is_authenticated:
            return

        db_cart, _ = Cart.objects.get_or_create(user=user)
        for item in self:
            product = item['product']
            cart_item, created = CartItem.objects.get_or_create(
                cart=db_cart,
                product=product,
                defaults={
                    'quantity': item['quantity'],
                    'price_at_addition': product.price
                }
            )
            if not created:
                cart_item.quantity = min(cart_item.quantity + item['quantity'], product.stock_quantity)
                cart_item.save()
