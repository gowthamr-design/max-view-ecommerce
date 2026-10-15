from django import forms
from django.contrib.auth.models import User
from apps.catalog.models import Product, Category, LookbookSlide
from apps.cart.models import Order
from apps.accounts.models import CustomerProfile


class ProductAdminForm(forms.ModelForm):
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            'placeholder': 'e.g. classic-tailored-linen-blazer (auto-generated if empty)',
        })
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'sku', 'description',
            'price', 'rating', 'stock_quantity', 'is_trending',
            'is_active', 'image', 'image_url'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'e.g. Classic Tailored Linen Blazer',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'e.g. classic-tailored-linen-blazer',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'e.g. MV-MEN-011',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs resize-none',
                'rows': 4,
                'placeholder': 'Detailed garment description and craftsmanship details...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': '499.00',
                'step': '0.01',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': '4.8',
                'step': '0.1',
                'min': '1.0',
                'max': '5.0',
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': '25',
                'min': '0',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'https://images.unsplash.com/...',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-700 focus:outline-none focus:border-brand-orange shadow-xs file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-xs file:font-bold file:bg-neutral-900 file:text-white hover:file:bg-brand-orange',
            }),
            'is_trending': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-brand-orange focus:ring-brand-orange border-neutral-300 rounded',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-brand-orange focus:ring-brand-orange border-neutral-300 rounded',
            }),
        }


class CategoryAdminForm(forms.ModelForm):
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            'placeholder': 'e.g. mens-wear (auto-generated if empty)',
        })
    )

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'display_order', 'is_active', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': "e.g. Men's Wear",
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'e.g. mens-wear',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs resize-none',
                'rows': 3,
                'placeholder': 'Category overview and aesthetic notes...',
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': '1',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-700 focus:outline-none focus:border-brand-orange shadow-xs file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-xs file:font-bold file:bg-neutral-900 file:text-white hover:file:bg-brand-orange',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-brand-orange focus:ring-brand-orange border-neutral-300 rounded',
            }),
        }


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'px-4 py-2 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 font-semibold focus:outline-none focus:border-brand-orange shadow-xs',
            }),
        }


class LookbookSlideForm(forms.ModelForm):
    class Meta:
        model = LookbookSlide
        fields = ['title', 'subtitle', 'category', 'display_order', 'is_active', 'image_url', 'image', 'link_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
                'placeholder': 'e.g. The Autumn / Winter Editorial',
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
                'placeholder': 'e.g. Transcendent luxury tailoring...',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
            }),
            'link_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-brand-orange focus:ring-brand-orange border-neutral-300 rounded',
            }),
        }


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            'placeholder': 'Last Name',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
            'placeholder': 'Email Address',
        })
    )

    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address_line1', 'city', 'state', 'postal_code']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'Telephone Number',
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'Street Address / Suite',
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'City',
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'State',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-white border border-neutral-300 rounded-lg text-sm text-neutral-900 focus:outline-none focus:border-brand-orange shadow-xs',
                'placeholder': 'Postal PIN Code',
            }),
        }
