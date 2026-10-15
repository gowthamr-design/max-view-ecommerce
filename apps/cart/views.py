import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse
from apps.catalog.models import Product
from .cart import SessionCart


class CartDetailView(View):
    def get(self, request):
        cart = SessionCart(request)
        return render(request, 'cart/cart_detail.html', {
            'cart': cart,
            'items': list(cart),
            'subtotal': cart.get_subtotal(),
            'shipping': cart.get_shipping_cost(),
            'grand_total': cart.get_grand_total(),
        })


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        # If user is not logged in, redirect to login page and preserve intended product/action
        if not request.user.is_authenticated:
            request.session['pending_cart_add'] = {
                'product_id': product.id,
                'quantity': quantity,
            }
            messages.info(request, "Please log in to add items to your shopping bag.")
            return redirect(f"{reverse('accounts:login')}?next={product.get_absolute_url()}")

        if product.stock_quantity < 1:
            messages.error(request, f"Sorry, {product.name} is currently out of stock.")
            return redirect(request.META.get('HTTP_REFERER', product.get_absolute_url()))

        cart = SessionCart(request)
        cart.add(product=product, quantity=quantity)

        # Sync to database for authenticated user
        cart.sync_to_database(request.user)

        messages.success(request, f"Added '{product.name}' to your shopping bag.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'cart_count': len(cart),
                'subtotal': str(cart.get_subtotal()),
                'message': f"Added '{product.name}' to shopping bag.",
            })

        return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        cart = SessionCart(request)

        cart.update(product=product, quantity=quantity)

        if request.user.is_authenticated:
            cart.sync_to_database(request.user)

        messages.success(request, f"Updated quantity for '{product.name}'.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'cart_count': len(cart),
                'subtotal': str(cart.get_subtotal()),
                'shipping': str(cart.get_shipping_cost()),
                'grand_total': str(cart.get_grand_total()),
            })

        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = SessionCart(request)
        cart.remove(product=product)

        messages.info(request, f"Removed '{product.name}' from your shopping bag.")
        return redirect('cart:cart_detail')


from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, CartItem


class CheckoutReviewView(LoginRequiredMixin, View):
    def get(self, request):
        cart = SessionCart(request)
        if len(cart) == 0:
            messages.warning(request, "Your shopping bag is empty. Please select pieces before checking out.")
            return redirect('catalog:category_list')

        return render(request, 'cart/checkout_review.html', {
            'cart': cart,
            'items': list(cart),
            'subtotal': cart.get_subtotal(),
            'shipping': cart.get_shipping_cost(),
            'grand_total': cart.get_grand_total(),
        })

    def post(self, request):
        cart = SessionCart(request)
        if len(cart) == 0:
            messages.warning(request, "Your shopping bag is empty.")
            return redirect('catalog:category_list')

        full_name = request.POST.get('full_name', '').strip() or request.user.get_full_name() or request.user.username
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        order_number = f"MV-{uuid.uuid4().hex[:8].upper()}"

        subtotal = cart.get_subtotal()
        shipping = cart.get_shipping_cost()
        grand_total = cart.get_grand_total()

        # Create Order in MySQL database
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            full_name=full_name,
            email=request.user.email,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            subtotal=subtotal,
            shipping=shipping,
            grand_total=grand_total,
            status=Order.STATUS_PENDING,
        )

        # Create OrderItems
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Update customer profile address if fields were blank
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            updated = False
            if phone and not profile.phone:
                profile.phone = phone
                updated = True
            if address and not profile.address_line1:
                profile.address_line1 = address
                updated = True
            if city and not profile.city:
                profile.city = city
                updated = True
            if postal_code and not profile.postal_code:
                profile.postal_code = postal_code
                updated = True
            if updated:
                profile.save()

        # Clear session and database cart
        cart.clear()
        CartItem.objects.filter(cart__user=request.user).delete()

        messages.success(request, f"Order #{order_number} confirmed! Thank you for choosing MAX VIEW.")

        return render(request, 'cart/checkout_success.html', {
            'order': order,
            'order_number': order_number,
            'full_name': full_name,
            'grand_total': grand_total,
        })

