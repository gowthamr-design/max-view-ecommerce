from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.db.models import Q
from apps.catalog.models import Product, Category
from apps.core.models import ContactMessage, NewsletterSubscriber
from apps.core.forms import ContactForm, NewsletterForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch 4 Trending Arrivals across categories (Men's, Women's, Kids', Accessories)
        context['trending_products'] = Product.objects.filter(
            is_trending=True,
            is_active=True
        ).select_related('category').order_by('category__display_order')[:4]
        
        # In case fewer than 4 are marked trending, backfill with active products
        if context['trending_products'].count() < 4:
            context['trending_products'] = Product.objects.filter(
                is_active=True
            ).select_related('category').order_by('category__display_order')[:4]

        context['categories'] = Category.objects.filter(is_active=True).order_by('display_order')[:4]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'core/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out. Our concierge team has received your message and will respond shortly.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors in the form below.")
            return render(request, 'core/contact.html', {'form': form})


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        products = Product.objects.none()
        
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query),
                is_active=True
            ).select_related('category')

        return render(request, 'core/search_results.html', {
            'query': query,
            'products': products,
            'result_count': products.count(),
        })


class NewsletterSubscribeView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                messages.success(request, "You have been subscribed to exclusive MAX VIEW collection releases.")
            else:
                messages.info(request, "You are already a valued subscriber to MAX VIEW updates.")
        else:
            messages.error(request, "Please provide a valid email address.")

        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
        return redirect(next_url)
