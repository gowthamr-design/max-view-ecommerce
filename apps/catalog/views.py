from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from .models import Category, Product, LookbookSlide


class CategoryListView(View):
    """
    Renders dedicated Categories showcase with lookbook carousel and category filtering.
    Guarantees strict category isolation without mixing unrelated products.
    """
    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by('display_order')
        selected_category_slug = request.GET.get('category')

        if selected_category_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug, is_active=True)
            products = Product.objects.filter(category=selected_category, is_active=True).select_related('category')[:10]
        else:
            selected_category = categories.first()
            if selected_category:
                products = Product.objects.filter(category=selected_category, is_active=True).select_related('category')[:10]
            else:
                products = Product.objects.none()

        lookbook_slides = LookbookSlide.objects.filter(is_active=True).order_by('display_order')

        return render(request, 'catalog/category_list.html', {
            'categories': categories,
            'selected_category': selected_category,
            'products': products,
            'lookbook_slides': lookbook_slides,
        })


class CategoryDetailView(View):
    """Displays products filtered strictly for a single category URL."""
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(category=category, is_active=True).select_related('category')[:10]
        categories = Category.objects.filter(is_active=True).order_by('display_order')
        lookbook_slides = LookbookSlide.objects.filter(is_active=True).order_by('display_order')

        return render(request, 'catalog/category_list.html', {
            'categories': categories,
            'selected_category': category,
            'products': products,
            'lookbook_slides': lookbook_slides,
        })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related products in the same category (excluding current)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context
