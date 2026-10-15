from django import forms
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white border border-neutral-300 rounded-sm focus:outline-none focus:border-neutral-900 text-neutral-900 placeholder-neutral-400 text-sm transition-colors',
            'placeholder': 'Subject',
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-neutral-300 rounded-sm focus:outline-none focus:border-neutral-900 text-neutral-900 placeholder-neutral-400 text-sm transition-colors',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-neutral-300 rounded-sm focus:outline-none focus:border-neutral-900 text-neutral-900 placeholder-neutral-400 text-sm transition-colors',
                'placeholder': 'Your Email',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border border-neutral-300 rounded-sm focus:outline-none focus:border-neutral-900 text-neutral-900 placeholder-neutral-400 text-sm transition-colors resize-none',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True,
            }),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        return subject.strip() if subject and subject.strip() else 'Customer Inquiry'



class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-luxury-charcoal text-luxury-cream placeholder-neutral-400 border border-neutral-700 rounded-sm focus:outline-none focus:border-luxury-gold text-sm transition-colors',
                'placeholder': 'Enter your email address',
                'required': True,
            }),
        }
