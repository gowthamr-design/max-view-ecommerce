from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    display_order = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        return 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=800&auto=format&fit=crop'


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        db_index=True
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    stock_quantity = models.PositiveIntegerField(default=100)
    is_trending = models.BooleanField(default=False, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Fallback external or static image URL")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_trending', '-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active'], name='idx_cat_active'),
            models.Index(fields=['is_trending', 'is_active'], name='idx_trending_active'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        """Returns the uploaded image URL, fallback URL, or placeholder."""
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=800&auto=format&fit=crop'

    @property
    def color_name(self):
        """Returns formatted color metadata matching reference images 4 & 5."""
        known_colors = {
            'arrow': 'Green & Black',
            'raymond': 'Pink & White',
            'louis philippe': 'Yellow & Black',
            'van heusen': 'Gray & Black',
            'allen solly': 'Yellow & White With Black',
            'peter england': 'Light Yellow & Brown',
            'park avenue': 'light blue & White',
            'mufti': 'Red & white',
            'indian terrain': 'Red & Black',
            'zodiac': 'White & Blue',
            'biba': 'Yellow & Red',
            'mumkins': 'Light Green',
            'peppermint': 'White With Green',
            'fabindia': 'Gray & Black',
            'gini': 'Light blue',
            'gini & jony': 'White & Pink',
            'janie and jack': 'Orange',
            'nike': 'Orange with dark',
            'zara': 'Pink & White',
            'gucci': 'RGB colors',
        }
        name_lower = self.name.lower()
        for key, val in known_colors.items():
            if key in name_lower:
                return val
        return 'Classic & Modern'



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Gallery Image for {self.product.name}"


class LookbookSlide(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='lookbook/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='slides'
    )
    link_url = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=1200&auto=format&fit=crop'
