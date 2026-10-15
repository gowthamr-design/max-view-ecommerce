from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Username'
        })
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Email'
        })
    )
    age = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Age'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists. Please log in.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please select another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Password'
        })
    )


class VerifyOTPForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-center tracking-[0.4em] text-xl sm:text-2xl font-mono font-bold transition-colors',
            'placeholder': '000000',
            'maxlength': '6',
            'autocomplete': 'one-time-code',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
        })
    )

    def clean_otp_code(self):
        code = self.cleaned_data.get('otp_code', '').strip()
        if not code.isdigit() or len(code) != 6:
            raise ValidationError("Please enter a valid 6-digit verification code.")
        return code


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Email Address'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').strip().lower()
        username = cleaned_data.get('username', '').strip()

        if email:
            qs = User.objects.filter(email__iexact=email)
            if username:
                qs = qs.filter(username__iexact=username)
                if not qs.exists():
                    self.add_error('username', "No account found matching this username and email address.")
                    return cleaned_data
            elif not qs.exists():
                self.add_error('email', "No registered account found with this email address.")
                return cleaned_data
        return cleaned_data


class ResetPasswordForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-center tracking-[0.4em] text-lg sm:text-xl font-mono font-bold transition-colors',
            'placeholder': '6-Digit OTP Code',
            'maxlength': '6',
            'inputmode': 'numeric',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'New Password'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white border border-neutral-900 px-4 py-3.5 text-neutral-900 placeholder:text-stone-400 focus:outline-none focus:border-black focus:ring-1 focus:ring-black rounded-none text-sm sm:text-base transition-colors',
            'placeholder': 'Confirm Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and len(password) < 8:
            self.add_error('password', "Password must contain at least 8 characters.")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

