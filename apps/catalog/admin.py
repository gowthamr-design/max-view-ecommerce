from django.contrib import admin
from .models import Category, Product, ProductImage, LookbookSlide


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sku', 'price', 'rating', 'stock_quantity', 'is_trending', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_trending', 'is_active')
    search_fields = ('name', 'sku', 'description')
    inlines = [ProductImageInline]


@admin.register(LookbookSlide)
class LookbookSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'display_order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'subtitle')
