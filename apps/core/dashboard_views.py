from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Count, Q, ProtectedError
from django.contrib.auth.models import User
from django.utils.text import slugify

from apps.catalog.models import Product, Category, LookbookSlide
from apps.cart.models import Order, OrderItem
from apps.accounts.models import CustomerProfile
from apps.core.models import ContactMessage, NewsletterSubscriber
from .dashboard_forms import (
    ProductAdminForm,
    CategoryAdminForm,
    OrderStatusUpdateForm,
    LookbookSlideForm,
)


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Enforces strict Role-Based Access Control (RBAC).
    Only authorized Admin users (is_staff or is_superuser) may access.
    Non-admin authenticated users are denied with HTTP 403 Forbidden.
    Unauthenticated visitors are redirected to the Login page.
    """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Please sign in with an administrator account.")
            return redirect(f"{reverse('accounts:login')}?next={self.request.path}")
        raise PermissionDenied("Access Denied: You do not have administrator permissions to view this resource.")


# ==============================================================================
# 1. ADMIN DASHBOARD OVERVIEW
# ==============================================================================
class DashboardHomeView(AdminRequiredMixin, View):
    def get(self, request):
        total_products = Product.objects.filter(is_active=True).count()
        total_categories = Category.objects.filter(is_active=True).count()
        total_orders = Order.objects.count()
        total_customers = User.objects.filter(is_staff=False).count()
        
        revenue_data = Order.objects.exclude(status=Order.STATUS_CANCELLED).aggregate(total=Sum('grand_total'))
        total_revenue = revenue_data['total'] or 0.00

        pending_orders_count = Order.objects.filter(status=Order.STATUS_PENDING).count()
        recent_orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')[:8]
        recent_customers = User.objects.filter(is_staff=False).order_by('-date_joined')[:6]
        recent_inquiries = ContactMessage.objects.filter(is_resolved=False).order_by('-created_at')[:5]

        return render(request, 'dashboard/dashboard_home.html', {
            'total_products': total_products,
            'total_categories': total_categories,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'pending_orders_count': pending_orders_count,
            'recent_orders': recent_orders,
            'recent_customers': recent_customers,
            'recent_inquiries': recent_inquiries,
        })


# ==============================================================================
# 2. PRODUCTS MANAGEMENT
# ==============================================================================
class AdminProductListView(AdminRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        category_slug = request.GET.get('category', '').strip()

        products = Product.objects.select_related('category').order_by('-created_at')

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query) |
                Q(description__icontains=query)
            )

        if category_slug:
            products = products.filter(category__slug=category_slug)

        categories = Category.objects.all().order_by('name')

        return render(request, 'dashboard/products_list.html', {
            'products': products,
            'categories': categories,
            'query': query,
            'selected_category': category_slug,
        })


class AdminProductCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = ProductAdminForm()
        return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add New Product'})

    def post(self, request):
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.slug:
                product.slug = slugify(product.name)
            base_slug = product.slug or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug
            product.save()
            messages.success(request, f"Product '{product.name}' was successfully created.")
            return redirect('dashboard:products_list')
        return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add New Product'})


class AdminProductUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductAdminForm(instance=product)
        return render(request, 'dashboard/product_form.html', {'form': form, 'product': product, 'title': f"Edit: {product.name}"})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            if not updated_product.slug:
                updated_product.slug = slugify(updated_product.name)
            base_slug = updated_product.slug or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            updated_product.slug = slug
            updated_product.save()
            messages.success(request, f"Product '{updated_product.name}' has been updated.")
            return redirect('dashboard:products_list')
        return render(request, 'dashboard/product_form.html', {'form': form, 'product': product, 'title': f"Edit: {product.name}"})


class AdminProductDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        name = product.name
        try:
            product.delete()
            messages.info(request, f"Product '{name}' has been deleted from catalog.")
        except ProtectedError:
            product.is_active = False
            product.save()
            messages.warning(request, f"Product '{name}' is part of historical customer orders and cannot be completely deleted. It has been deactivated and hidden from the storefront.")
        return redirect('dashboard:products_list')


# ==============================================================================
# 3. CATEGORIES MANAGEMENT
# ==============================================================================
class AdminCategoryListView(AdminRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('products')).order_by('display_order', 'name')
        return render(request, 'dashboard/categories_list.html', {'categories': categories})


class AdminCategoryCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = CategoryAdminForm()
        return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add New Category'})

    def post(self, request):
        form = CategoryAdminForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            if not category.slug:
                category.slug = slugify(category.name)
            base_slug = category.slug or 'category'
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            category.slug = slug
            category.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
            return redirect('dashboard:categories_list')
        return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add New Category'})


class AdminCategoryUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryAdminForm(instance=category)
        return render(request, 'dashboard/category_form.html', {'form': form, 'category': category, 'title': f"Edit: {category.name}"})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryAdminForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            updated_category = form.save(commit=False)
            if not updated_category.slug:
                updated_category.slug = slugify(updated_category.name)
            base_slug = updated_category.slug or 'category'
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=category.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            updated_category.slug = slug
            updated_category.save()
            messages.success(request, f"Category '{updated_category.name}' has been updated.")
            return redirect('dashboard:categories_list')
        return render(request, 'dashboard/category_form.html', {'form': form, 'category': category, 'title': f"Edit: {category.name}"})


class AdminCategoryDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.products.exists():
            messages.error(request, f"Cannot delete '{category.name}' because it contains active products. Please reassign or delete its products first.")
            return redirect('dashboard:categories_list')
        name = category.name
        category.delete()
        messages.info(request, f"Category '{name}' has been removed.")
        return redirect('dashboard:categories_list')


# ==============================================================================
# 4. ORDERS MANAGEMENT
# ==============================================================================
class AdminOrderListView(AdminRequiredMixin, View):
    def get(self, request):
        status_filter = request.GET.get('status', 'all').strip().lower()
        orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')

        if status_filter and status_filter != 'all':
            orders = orders.filter(status=status_filter)

        status_counts = {
            'all': Order.objects.count(),
            'pending': Order.objects.filter(status=Order.STATUS_PENDING).count(),
            'processing': Order.objects.filter(status=Order.STATUS_PROCESSING).count(),
            'shipped': Order.objects.filter(status=Order.STATUS_SHIPPED).count(),
            'delivered': Order.objects.filter(status=Order.STATUS_DELIVERED).count(),
            'cancelled': Order.objects.filter(status=Order.STATUS_CANCELLED).count(),
        }

        return render(request, 'dashboard/orders_list.html', {
            'orders': orders,
            'current_status': status_filter,
            'status_counts': status_counts,
        })


class AdminOrderDetailView(AdminRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.select_related('user').prefetch_related('items__product'), pk=pk)
        status_form = OrderStatusUpdateForm(instance=order)
        return render(request, 'dashboard/order_detail.html', {
            'order': order,
            'status_form': status_form,
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status_form = OrderStatusUpdateForm(request.POST, instance=order)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, f"Order #{order.order_number} status updated to {order.get_status_display()}.")
            return redirect('dashboard:order_detail', pk=pk)
        return render(request, 'dashboard/order_detail.html', {
            'order': order,
            'status_form': status_form,
        })


class AdminOrderDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        num = order.order_number
        order.delete()
        messages.info(request, f"Order #{num} has been deleted.")
        return redirect('dashboard:orders_list')


# ==============================================================================
# 5. CUSTOMER ACCOUNTS MANAGEMENT
# ==============================================================================
class AdminCustomerListView(AdminRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        customers = User.objects.filter(is_staff=False).select_related('profile').annotate(
            orders_count=Count('orders'),
            total_spent=Sum('orders__grand_total')
        ).order_by('-date_joined')

        if query:
            customers = customers.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        return render(request, 'dashboard/customers_list.html', {
            'customers': customers,
            'query': query,
        })


class AdminCustomerDetailView(AdminRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(User.objects.select_related('profile'), pk=pk, is_staff=False)
        customer_orders = customer.orders.all().prefetch_related('items__product').order_by('-created_at')
        total_spent = customer_orders.exclude(status=Order.STATUS_CANCELLED).aggregate(total=Sum('grand_total'))['total'] or 0.00

        return render(request, 'dashboard/customer_detail.html', {
            'customer': customer,
            'orders': customer_orders,
            'total_spent': total_spent,
        })


class AdminCustomerToggleStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(User, pk=pk, is_staff=False)
        customer.is_active = not customer.is_active
        customer.save()
        status_label = "activated" if customer.is_active else "deactivated"
        messages.success(request, f"Customer account @{customer.username} has been {status_label}.")
        return redirect(request.META.get('HTTP_REFERER') or 'dashboard:customers_list')


class AdminCustomerDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(User, pk=pk, is_staff=False)
        username = customer.username
        customer.delete()
        messages.info(request, f"Customer account @{username} has been permanently deleted.")
        return redirect('dashboard:customers_list')



# ==============================================================================
# 6. WEBSITE CONTENT MANAGEMENT
# ==============================================================================
class AdminContentManagementView(AdminRequiredMixin, View):
    def get(self, request):
        slides = LookbookSlide.objects.select_related('category').order_by('display_order', 'id')
        messages_list = ContactMessage.objects.all().order_by('-created_at')[:20]
        subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')[:30]
        slide_form = LookbookSlideForm()

        return render(request, 'dashboard/content_management.html', {
            'slides': slides,
            'messages_list': messages_list,
            'subscribers': subscribers,
            'slide_form': slide_form,
        })


class AdminSlideCreateView(AdminRequiredMixin, View):
    def post(self, request):
        form = LookbookSlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save()
            messages.success(request, f"Lookbook Slide '{slide.title}' added successfully.")
        else:
            messages.error(request, "Failed to create slide. Please check form values.")
        return redirect('dashboard:content_management')


class AdminSlideDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        slide = get_object_or_404(LookbookSlide, pk=pk)
        title = slide.title
        slide.delete()
        messages.info(request, f"Slide '{title}' was deleted.")
        return redirect('dashboard:content_management')


class AdminContactResolveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        contact = get_object_or_404(ContactMessage, pk=pk)
        contact.is_resolved = not contact.is_resolved
        contact.save()
        status_text = "resolved" if contact.is_resolved else "unresolved"
        messages.success(request, f"Inquiry from {contact.name} marked as {status_text}.")
        return redirect('dashboard:content_management')
