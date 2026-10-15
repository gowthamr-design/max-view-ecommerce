from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import (
    CustomerRegistrationForm,
    CustomerLoginForm,
    VerifyOTPForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from .models import EmailOTP
from .utils import create_email_otp, send_otp_email
from apps.catalog.models import Product
from apps.cart.cart import SessionCart


class CustomerRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = CustomerRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            username = form.cleaned_data['username'].strip()
            first_name = form.cleaned_data['first_name'].strip()
            last_name = form.cleaned_data.get('last_name', '').strip()
            age = form.cleaned_data.get('age')
            password = form.cleaned_data['password']

            # Stash registration details safely in session until OTP is confirmed
            session_payload = {
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'username': username,
                'email': email,
                'password': password,
            }
            request.session['pending_registration'] = session_payload
            request.session['pending_otp_email'] = email
            request.session['pending_otp_purpose'] = EmailOTP.PURPOSE_REGISTRATION

            # Generate OTP & Send via SMTP
            otp_obj = create_email_otp(
                email=email,
                purpose=EmailOTP.PURPOSE_REGISTRATION,
                session_data={'first_name': first_name, 'username': username}
            )
            email_sent = send_otp_email(
                email=email,
                otp_code=otp_obj.otp_code,
                purpose=EmailOTP.PURPOSE_REGISTRATION,
                user_name=first_name
            )

            if email_sent:
                messages.success(request, f"A 6-digit verification code has been sent to {email}. Please enter it below to activate your account.")
            else:
                messages.warning(
                    request,
                    f"A verification code was generated for {email}. (Note: If using local development without SMTP credentials, check console logs for the OTP)."
                )

            return redirect('accounts:verify_otp')
        else:
            return render(request, 'accounts/register.html', {'form': form})


class VerifyOTPView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')

        email = request.session.get('pending_otp_email')
        purpose = request.session.get('pending_otp_purpose', EmailOTP.PURPOSE_REGISTRATION)

        if not email:
            messages.info(request, "Please register or request a password reset code first.")
            return redirect('accounts:register')

        form = VerifyOTPForm()
        return render(request, 'accounts/verify_otp.html', {
            'form': form,
            'email': email,
            'purpose': purpose,
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')

        email = request.session.get('pending_otp_email')
        purpose = request.session.get('pending_otp_purpose', EmailOTP.PURPOSE_REGISTRATION)

        if not email:
            messages.error(request, "Session expired. Please start registration again.")
            return redirect('accounts:register')

        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp_code']

            # Find matching active OTP
            otp_records = EmailOTP.objects.filter(
                email=email,
                purpose=purpose,
                is_verified=False
            ).order_by('-created_at')

            if not otp_records.exists():
                form.add_error('otp_code', "No pending OTP request found. Please request a new code.")
                return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})

            latest_otp = otp_records.first()

            if latest_otp.is_expired():
                form.add_error('otp_code', "This verification code has expired. Please click 'Resend OTP'.")
                return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})

            if latest_otp.otp_code != otp_input:
                form.add_error('otp_code', "Incorrect verification code. Please try again.")
                return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})

            # OTP verified successfully!
            latest_otp.is_verified = True
            latest_otp.save()

            if purpose == EmailOTP.PURPOSE_REGISTRATION:
                reg_data = request.session.get('pending_registration')
                if not reg_data:
                    messages.error(request, "Registration session data lost. Please register again.")
                    return redirect('accounts:register')

                # Create the user in MySQL database
                user = User.objects.create_user(
                    username=reg_data['username'],
                    email=reg_data['email'],
                    password=reg_data['password'],
                    first_name=reg_data.get('first_name', ''),
                    last_name=reg_data.get('last_name', '')
                )

                # Authenticate and login
                login(request, user)

                # Process pending cart add if preserved
                pending_cart_add = request.session.pop('pending_cart_add', None)
                cart = SessionCart(request)
                if pending_cart_add:
                    try:
                        p = Product.objects.get(id=pending_cart_add['product_id'], is_active=True)
                        q = pending_cart_add.get('quantity', 1)
                        cart.add(product=p, quantity=q)
                        messages.success(request, f"Added '{p.name}' to your shopping bag.")
                    except Product.DoesNotExist:
                        pass

                # Sync session cart
                cart.sync_to_database(user)

                # Clean up session keys
                request.session.pop('pending_registration', None)
                request.session.pop('pending_otp_email', None)
                request.session.pop('pending_otp_purpose', None)

                messages.success(request, f"Email verified successfully! Welcome to MAX VIEW, {user.first_name or user.username}!")
                if pending_cart_add:
                    return redirect('cart:cart_detail')
                return redirect('core:home')

            elif purpose == EmailOTP.PURPOSE_PASSWORD_RESET:
                request.session['verified_reset_email'] = email
                return redirect('accounts:reset_password')

        return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})


class ResendOTPView(View):
    def post(self, request):
        email = request.session.get('pending_otp_email')
        purpose = request.session.get('pending_otp_purpose', EmailOTP.PURPOSE_REGISTRATION)

        if not email:
            messages.error(request, "Session expired. Please start over.")
            return redirect('accounts:register')

        # Generate fresh OTP and send via SMTP
        otp_obj = create_email_otp(email=email, purpose=purpose)
        email_sent = send_otp_email(
            email=email,
            otp_code=otp_obj.otp_code,
            purpose=purpose
        )

        if email_sent:
            messages.success(request, f"A fresh verification code has been dispatched to {email}.")
        else:
            messages.info(request, f"New code generated. If in local development, check console logs.")

        return redirect('accounts:verify_otp')


class ForgotPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = ForgotPasswordForm()
        return render(request, 'accounts/forgot_password.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            username = form.cleaned_data.get('username', '').strip()

            qs = User.objects.filter(email__iexact=email)
            if username:
                qs = qs.filter(username__iexact=username)
            user = qs.first()

            if not user:
                form.add_error(None, "No registered account matches the provided credentials.")
                return render(request, 'accounts/forgot_password.html', {'form': form})

            # Generate OTP for password reset
            otp_obj = create_email_otp(
                email=email,
                purpose=EmailOTP.PURPOSE_PASSWORD_RESET,
                session_data={'user_id': user.id}
            )

            email_sent = send_otp_email(
                email=email,
                otp_code=otp_obj.otp_code,
                purpose=EmailOTP.PURPOSE_PASSWORD_RESET,
                user_name=user.first_name
            )

            request.session['pending_otp_email'] = email
            request.session['pending_otp_purpose'] = EmailOTP.PURPOSE_PASSWORD_RESET

            if email_sent:
                messages.success(request, f"Password reset OTP sent to {email}. Please verify below.")
            else:
                messages.info(request, f"Password reset OTP generated for {email}.")

            return redirect('accounts:reset_password')
        return render(request, 'accounts/forgot_password.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        email = request.session.get('pending_otp_email') or request.session.get('verified_reset_email')
        if not email:
            messages.error(request, "Please request a password reset code first.")
            return redirect('accounts:forgot_password')

        form = ResetPasswordForm()
        return render(request, 'accounts/reset_password.html', {'form': form, 'email': email})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        email = request.session.get('pending_otp_email') or request.session.get('verified_reset_email')
        if not email:
            messages.error(request, "Session expired. Please request a new password reset.")
            return redirect('accounts:forgot_password')

        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp_code']
            new_password = form.cleaned_data['password']

            # Verify OTP
            otp_records = EmailOTP.objects.filter(
                email=email,
                purpose=EmailOTP.PURPOSE_PASSWORD_RESET,
                is_verified=False
            ).order_by('-created_at')

            if not otp_records.exists():
                form.add_error('otp_code', "No active password reset request found.")
                return render(request, 'accounts/reset_password.html', {'form': form, 'email': email})

            latest_otp = otp_records.first()
            if latest_otp.is_expired():
                form.add_error('otp_code', "This reset code has expired. Please request a new one.")
                return render(request, 'accounts/reset_password.html', {'form': form, 'email': email})

            if latest_otp.otp_code != otp_input:
                form.add_error('otp_code', "Incorrect verification code.")
                return render(request, 'accounts/reset_password.html', {'form': form, 'email': email})

            # Update password
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                latest_otp.is_verified = True
                latest_otp.save()

                # Clean up session
                request.session.pop('pending_otp_email', None)
                request.session.pop('pending_otp_purpose', None)
                request.session.pop('verified_reset_email', None)

                messages.success(request, "Password has been successfully updated! You can now sign in.")
                return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, "User account not found.")
                return redirect('accounts:forgot_password')

        return render(request, 'accounts/reset_password.html', {'form': form, 'email': email})


class CustomerLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = CustomerLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Support login with either username or email
            user = authenticate(request, username=login_input, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email=login_input)
                    user = authenticate(request, username=user_obj.username, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    user = None

            if user is not None:
                login(request, user)
                
                # Check for pending cart add preserved before login
                pending_cart_add = request.session.pop('pending_cart_add', None)
                cart = SessionCart(request)
                if pending_cart_add:
                    try:
                        p = Product.objects.get(id=pending_cart_add['product_id'], is_active=True)
                        q = pending_cart_add.get('quantity', 1)
                        cart.add(product=p, quantity=q)
                        messages.success(request, f"Added '{p.name}' to your shopping bag.")
                    except Product.DoesNotExist:
                        pass

                # Reconcile and sync guest session cart into user's DB cart
                cart.sync_to_database(user)

                messages.success(request, f"Welcome back, {user.first_name or user.username}!")

                if pending_cart_add:
                    return redirect('cart:cart_detail')

                next_url = request.POST.get('next') or request.GET.get('next') or 'core:home'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password.")
        return render(request, 'accounts/login.html', {'form': form})


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been securely signed out of MAX VIEW.")
        return redirect('core:home')

    def post(self, request):
        logout(request)
        messages.info(request, "You have been securely signed out of MAX VIEW.")
        return redirect('core:home')


from apps.cart.models import Order
from apps.core.dashboard_forms import UserProfileUpdateForm


class CustomerProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        orders = request.user.orders.all().prefetch_related('items__product').order_by('-created_at')
        form = UserProfileUpdateForm(
            instance=profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )
        return render(request, 'accounts/profile.html', {
            'user': request.user,
            'profile': profile,
            'orders': orders,
            'form': form,
        })

    def post(self, request):
        profile = getattr(request.user, 'profile', None)
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name', '').strip()
            last_name = form.cleaned_data.get('last_name', '').strip()
            email = form.cleaned_data.get('email', '').strip()

            # Check email uniqueness if modified
            if email and email != request.user.email and User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.error(request, "This email is already in use by another account.")
                orders = request.user.orders.all().prefetch_related('items__product').order_by('-created_at')
                return render(request, 'accounts/profile.html', {
                    'user': request.user,
                    'profile': profile,
                    'orders': orders,
                    'form': form,
                })

            request.user.first_name = first_name
            request.user.last_name = last_name
            if email:
                request.user.email = email
            request.user.save()

            if profile:
                profile.phone = form.cleaned_data.get('phone')
                profile.address_line1 = form.cleaned_data.get('address_line1')
                profile.city = form.cleaned_data.get('city')
                profile.state = form.cleaned_data.get('state')
                profile.postal_code = form.cleaned_data.get('postal_code')
                profile.save()

            messages.success(request, "Your personal information has been successfully updated.")
            return redirect('accounts:profile')

        orders = request.user.orders.all().prefetch_related('items__product').order_by('-created_at')
        return render(request, 'accounts/profile.html', {
            'user': request.user,
            'profile': profile,
            'orders': orders,
            'form': form,
        })


class UserOrderDetailView(LoginRequiredMixin, View):
    """
    Object-level security: Users can only view their own orders.
    Attempting to view an order belonging to another customer returns HTTP 404.
    """
    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.prefetch_related('items__product'),
            pk=pk,
            user=request.user
        )
        return render(request, 'accounts/order_detail.html', {
            'order': order,
        })


