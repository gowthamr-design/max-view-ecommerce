from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default='MAX VIEW')
    support_email = models.EmailField(default='maxview1@gmail.com')
    support_phone = models.CharField(max_length=50, default='1234567890')
    store_address = models.TextField(default='123@ Tirupur, Tamil Nadu, Old Bus Stand Tirupur, INDIA')
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=999.00)

    def __str__(self):
        return self.site_name
