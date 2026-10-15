from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product
from apps.core.models import ContactMessage, NewsletterSubscriber
from apps.accounts.models import EmailOTP
from apps.cart.models import Order, OrderItem


class MaxViewE2ETests(TestCase):
    """
    Comprehensive verification tests for MAX VIEW Luxury E-Commerce website.
    """

    def setUp(self):
        self.client = Client()

        # Seed test category
        self.category = Category.objects.create(
            name="Men's Wear",
            slug="mens-wear",
            description="Luxury tailoring for men.",
            display_order=1,
            is_active=True
        )

        # Seed test product
        self.product = Product.objects.create(
            category=self.category,
            name="Classic Tailored Linen Blazer",
            slug="classic-tailored-linen-blazer",
            sku="MV-MEN-TEST",
            description="A luxury tailored linen blazer.",
            price=499.00,
            rating=4.8,
            stock_quantity=10,
            is_trending=True,
            is_active=True
        )

    def test_fr01_home_page_renders_with_brand_and_trending(self):
        """FR-01, FR-02: Test Home page exhibits brand header, hero, trending products, benefits."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MAX VIEW")
        self.assertContains(response, "Trending Arrivals")
        self.assertContains(response, "Classic Tailored Linen Blazer")
        self.assertContains(response, "₹499.00")
        self.assertContains(response, "Free Shipping")

    def test_fr04_category_page_and_isolation(self):
        """FR-04, FR-05: Test Categories page loads with products and category filtering."""
        response = self.client.get(reverse('catalog:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Men&#x27;s Wear")

        detail_response = self.client.get(reverse('catalog:category_detail', kwargs={'slug': 'mens-wear'}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Classic Tailored Linen Blazer")

    def test_product_detail_page(self):
        """FR-03, FR-14: Test single product detail view."""
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Tailored Linen Blazer")
        self.assertContains(response, "₹499.00")
        self.assertContains(response, "Add to Shopping Bag")

    def test_fr06_about_page_content(self):
        """FR-06: Test About Us page renders exact brand story and mission."""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABOUT US")
        self.assertContains(response, "Max Collection was founded with a passion")
        self.assertContains(response, "Our mission at Max Collection")

    def test_fr06_fr09_contact_page_and_form_submission(self):
        """FR-06, FR-09: Test Contact Us page, store info, careers anchor, and form submission."""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Old Bus Stand Tirupur")
        self.assertContains(response, "Careers at Forever")

        post_data = {
            'name': 'Gowtham Tester',
            'email': 'tester@example.com',
            'subject': 'Bespoke Inquiries',
            'message': 'Inquiring about autumn collection fittings.',
        }
        post_response = self.client.post(reverse('core:contact'), post_data, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='tester@example.com').exists())

    def test_fr11_search_functionality(self):
        """FR-11: Test keyword search matching and zero-match fallback."""
        # Query matching product
        response = self.client.get(reverse('core:search') + '?q=Linen')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Tailored Linen Blazer")

        # Zero match query
        empty_response = self.client.get(reverse('core:search') + '?q=NonExistentPiece999')
        self.assertEqual(empty_response.status_code, 200)
        self.assertContains(empty_response, "No silhouettes found matching")
        self.assertContains(empty_response, "Explore All Categories")

    def test_fr08_cart_lifecycle(self):
        """FR-08: Test cart add, quantity stepper update, subtotal, and remove for logged-in user and guest redirect."""
        # 1. Unauthenticated user is redirected to login with next param
        guest_add_response = self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2}
        )
        self.assertEqual(guest_add_response.status_code, 302)
        self.assertIn(reverse('accounts:login'), guest_add_response.url)
        self.assertIn('next=', guest_add_response.url)

        # 2. Authenticate user
        user = User.objects.create_user(username='couture_client', password='Password123!')
        self.client.login(username='couture_client', password='Password123!')

        # 3. Add to cart as logged-in user
        add_response = self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2},
            follow=True
        )
        self.assertEqual(add_response.status_code, 200)

        # Inspect cart view
        cart_view = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(cart_view, "Classic Tailored Linen Blazer")
        self.assertContains(cart_view, "₹998.00")  # 2 x 499

        # Update quantity
        update_response = self.client.post(
            reverse('cart:cart_update', kwargs={'product_id': self.product.id}),
            {'quantity': 1},
            follow=True
        )
        self.assertContains(update_response, "₹499.00")

        # Remove item
        remove_response = self.client.post(
            reverse('cart:cart_remove', kwargs={'product_id': self.product.id}),
            follow=True
        )
        self.assertContains(remove_response, "Your Shopping Bag is Empty")

    def test_pending_cart_preserved_after_login(self):
        """Test that guest attempting to add to cart gets redirected to login, and item is added upon successful login."""
        # 1. Guest attempts to add product
        guest_resp = self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 3}
        )
        self.assertEqual(guest_resp.status_code, 302)
        self.assertIn(reverse('accounts:login'), guest_resp.url)

        # 2. User logs in
        User.objects.create_user(username='pending_user', password='Password123!')
        login_resp = self.client.post(reverse('accounts:login'), {
            'username': 'pending_user',
            'password': 'Password123!'
        }, follow=True)
        self.assertEqual(login_resp.status_code, 200)

        # 3. Verify item was added to the cart and viewable
        cart_view = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(cart_view, "Classic Tailored Linen Blazer")
        self.assertContains(cart_view, "₹1497.00")

    def test_fr07_auth_registration_and_login(self):
        """FR-07, FR-12: Test user registration with Email OTP, verification, login, and logout."""
        # 1. Initial registration submission dispatches OTP to email
        reg_data = {
            'first_name': 'Alexander',
            'username': 'alexander_couture',
            'email': 'alexander@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
        }
        reg_response = self.client.post(reverse('accounts:register'), reg_data, follow=True)
        self.assertEqual(reg_response.status_code, 200)
        self.assertContains(reg_response, "Verification Code")

        # 2. Verify OTP was saved in database
        otp_record = EmailOTP.objects.filter(
            email='alexander@example.com',
            purpose=EmailOTP.PURPOSE_REGISTRATION
        ).order_by('-created_at').first()
        self.assertIsNotNone(otp_record)
        self.assertEqual(len(otp_record.otp_code), 6)

        # 3. Submit OTP verification to finalize account creation
        verify_response = self.client.post(reverse('accounts:verify_otp'), {
            'otp_code': otp_record.otp_code,
        }, follow=True)
        self.assertEqual(verify_response.status_code, 200)
        self.assertTrue(User.objects.filter(username='alexander_couture').exists())

        # 4. Logout
        logout_response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(logout_response.status_code, 200)

        # 5. Login with verified account
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'alexander_couture',
            'password': 'StrongPassword123!',
        }, follow=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, "alexander_couture")

    def test_forgot_password_and_reset_flow(self):
        """Test forgot password request, OTP dispatch, and reset password flow."""
        # Create test user
        User.objects.create_user(username='julian_vane', email='julian@example.com', password='OldPassword123!')

        # Request forgot password OTP
        forgot_response = self.client.post(reverse('accounts:forgot_password'), {
            'email': 'julian@example.com',
        }, follow=True)
        self.assertEqual(forgot_response.status_code, 200)
        self.assertContains(forgot_response, "Reset Your Password")

        # Retrieve OTP record
        otp_record = EmailOTP.objects.filter(
            email='julian@example.com',
            purpose=EmailOTP.PURPOSE_PASSWORD_RESET
        ).order_by('-created_at').first()
        self.assertIsNotNone(otp_record)

        # Submit password reset with OTP
        reset_response = self.client.post(reverse('accounts:reset_password'), {
            'otp_code': otp_record.otp_code,
            'new_password': 'NewPassword123!',
            'confirm_password': 'NewPassword123!',
        }, follow=True)
        self.assertEqual(reset_response.status_code, 200)

        # Verify user can log in with new password
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'julian_vane',
            'password': 'NewPassword123!',
        }, follow=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, "julian_vane")

    def test_newsletter_subscription(self):
        """FR-10: Test footer newsletter subscription."""
        sub_response = self.client.post(reverse('core:newsletter_subscribe'), {
            'email': 'vip_subscriber@example.com'
        }, follow=True)
        self.assertEqual(sub_response.status_code, 200)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='vip_subscriber@example.com').exists())

    def test_admin_rbac_access_and_crud(self):
        """Verify Admin can access dashboard and perform full CRUD on products and categories."""
        admin_user = User.objects.create_superuser(
            username='executive_admin',
            email='admin@test.com',
            password='AdminPassword123!'
        )
        self.client.login(username='executive_admin', password='AdminPassword123!')

        # 1. Admin accesses dashboard overview
        dash_response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Executive Overview")

        # 2. Admin adds a product
        create_resp = self.client.post(reverse('dashboard:product_create'), {
            'name': 'Bespoke Cashmere Overcoat',
            'slug': 'bespoke-cashmere-overcoat',
            'sku': 'MV-TEST-COAT-01',
            'category': self.category.id,
            'description': 'Handcrafted pure cashmere luxury overcoat.',
            'price': '1499.00',
            'rating': '5.0',
            'stock_quantity': '15',
            'is_trending': True,
            'is_active': True,
        }, follow=True)
        self.assertEqual(create_resp.status_code, 200)
        self.assertTrue(Product.objects.filter(sku='MV-TEST-COAT-01').exists())

        # 3. Admin updates the product
        new_prod = Product.objects.get(sku='MV-TEST-COAT-01')
        update_resp = self.client.post(reverse('dashboard:product_update', kwargs={'pk': new_prod.pk}), {
            'name': 'Bespoke Cashmere Overcoat (Updated)',
            'slug': 'bespoke-cashmere-overcoat',
            'sku': 'MV-TEST-COAT-01',
            'category': self.category.id,
            'description': 'Updated description.',
            'price': '1599.00',
            'rating': '5.0',
            'stock_quantity': '20',
            'is_active': True,
        }, follow=True)
        self.assertEqual(update_resp.status_code, 200)
        new_prod.refresh_from_db()
        self.assertEqual(new_prod.price, 1599.00)

        # 4. Admin deletes the product
        delete_resp = self.client.post(reverse('dashboard:product_delete', kwargs={'pk': new_prod.pk}), follow=True)
        self.assertEqual(delete_resp.status_code, 200)
        self.assertFalse(Product.objects.filter(sku='MV-TEST-COAT-01').exists())

    def test_non_admin_rbac_forbidden(self):
        """Verify normal users CANNOT access admin dashboard or execute management operations (HTTP 403 Forbidden)."""
        normal_user = User.objects.create_user(
            username='standard_shopper',
            email='shopper@test.com',
            password='Password123!'
        )
        self.client.login(username='standard_shopper', password='Password123!')

        # 1. Dashboard overview access denied
        overview_resp = self.client.get(reverse('dashboard:home'))
        self.assertEqual(overview_resp.status_code, 403)

        # 2. Product create form access denied
        create_get_resp = self.client.get(reverse('dashboard:product_create'))
        self.assertEqual(create_get_resp.status_code, 403)

        # 3. Product create POST endpoint rejected
        create_post_resp = self.client.post(reverse('dashboard:product_create'), {
            'name': 'Hacker Product',
            'sku': 'HACK-01',
            'price': '1.00',
        })
        self.assertEqual(create_post_resp.status_code, 403)
        self.assertFalse(Product.objects.filter(name='Hacker Product').exists())

        # 4. Category and Orders admin pages rejected
        self.assertEqual(self.client.get(reverse('dashboard:categories_list')).status_code, 403)
        self.assertEqual(self.client.get(reverse('dashboard:orders_list')).status_code, 403)

    def test_unauthenticated_admin_redirect(self):
        """Verify unauthenticated visitors to admin URLs are redirected to login with next parameter."""
        resp = self.client.get(reverse('dashboard:home'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('accounts:login'), resp.url)
        self.assertIn('next=', resp.url)

    def test_user_order_object_level_security_and_profile_update(self):
        """Verify user order creation on checkout, object-level isolation, and profile update."""
        user_a = User.objects.create_user(username='client_a', email='client_a@test.com', password='Password123!')
        user_b = User.objects.create_user(username='client_b', email='client_b@test.com', password='Password123!')

        # 1. User A adds item and checks out
        self.client.login(username='client_a', password='Password123!')
        self.client.post(reverse('cart:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})

        checkout_resp = self.client.post(reverse('cart:checkout'), {
            'full_name': 'Client A Full',
            'phone': '+91 9988776655',
            'address': '42 Heritage Boulevard',
            'city': 'Tirupur',
            'postal_code': '641601',
        }, follow=True)
        self.assertEqual(checkout_resp.status_code, 200)

        # Verify Order was created in database
        order_a = Order.objects.filter(user=user_a).first()
        self.assertIsNotNone(order_a)
        self.assertEqual(order_a.items.count(), 1)

        # 2. User A can view their own order
        user_a_order_view = self.client.get(reverse('accounts:order_detail', kwargs={'pk': order_a.pk}))
        self.assertEqual(user_a_order_view.status_code, 200)
        self.assertContains(user_a_order_view, order_a.order_number)

        # 3. User B logs in and tries to access User A's order -> HTTP 404 (Object-level security)
        self.client.login(username='client_b', password='Password123!')
        unauthorized_order_view = self.client.get(reverse('accounts:order_detail', kwargs={'pk': order_a.pk}))
        self.assertEqual(unauthorized_order_view.status_code, 404)

        # 4. User B updates their personal information
        profile_update_resp = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Julian',
            'last_name': 'Bespoke',
            'email': 'client_b_updated@test.com',
            'phone': '+91 9123456789',
            'address_line1': '100 King Cross',
            'city': 'Coimbatore',
            'state': 'Tamil Nadu',
            'postal_code': '641001',
        }, follow=True)
        self.assertEqual(profile_update_resp.status_code, 200)
        user_b.refresh_from_db()
        self.assertEqual(user_b.first_name, 'Julian')
        self.assertEqual(user_b.email, 'client_b_updated@test.com')
        self.assertEqual(user_b.profile.city, 'Coimbatore')

    def test_auth_pages_reference_design_and_validation(self):
        """Verify Login, Sign Up, and Forgot Password reference design fields and validations."""
        # 1. Login Page GET
        login_page = self.client.get(reverse('accounts:login'))
        self.assertEqual(login_page.status_code, 200)
        self.assertContains(login_page, "Login")
        self.assertContains(login_page, "Forgot your password?")
        self.assertContains(login_page, "Create account")

        # 2. Login invalid credentials
        invalid_login = self.client.post(reverse('accounts:login'), {
            'username': 'nonexistent_user',
            'password': 'WrongPassword123!',
        })
        self.assertEqual(invalid_login.status_code, 200)
        self.assertContains(invalid_login, "Invalid username/email or password")

        # 3. Sign Up Page GET
        register_page = self.client.get(reverse('accounts:register'))
        self.assertEqual(register_page.status_code, 200)
        self.assertContains(register_page, "Sign Up")
        self.assertContains(register_page, "Already have an account?")
        self.assertContains(register_page, "placeholder=\"Username\"")
        self.assertContains(register_page, "placeholder=\"First Name\"")
        self.assertContains(register_page, "placeholder=\"Last Name\"")
        self.assertContains(register_page, "placeholder=\"Email\"")
        self.assertContains(register_page, "placeholder=\"Age\"")
        self.assertContains(register_page, "placeholder=\"Password\"")
        self.assertContains(register_page, "placeholder=\"Confirm Password\"")

        # 4. Sign Up Duplicate Email validation
        User.objects.create_user(username='existing_client', email='duplicate@example.com', password='Password123!')
        dup_reg = self.client.post(reverse('accounts:register'), {
            'username': 'new_client_attempt',
            'first_name': 'New',
            'last_name': 'Client',
            'email': 'duplicate@example.com',
            'age': 28,
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        })
        self.assertEqual(dup_reg.status_code, 200)
        self.assertContains(dup_reg, "An account with this email address already exists. Please log in.")

        # 5. Forgot Password Page GET (matches Image 3)
        forgot_page = self.client.get(reverse('accounts:forgot_password'))
        self.assertEqual(forgot_page.status_code, 200)
        self.assertContains(forgot_page, "Forgot Password")
        self.assertContains(forgot_page, "Enter your username and email to receive an OTP.")
        self.assertContains(forgot_page, "placeholder=\"Username\"")
        self.assertContains(forgot_page, "placeholder=\"Email Address\"")
        self.assertContains(forgot_page, "Send OTP")
        self.assertContains(forgot_page, "Back to Login")

        # 6. Forgot Password POST with Username + Email
        forgot_post = self.client.post(reverse('accounts:forgot_password'), {
            'username': 'existing_client',
            'email': 'duplicate@example.com',
        }, follow=True)
        self.assertEqual(forgot_post.status_code, 200)
        self.assertContains(forgot_post, "Reset Your Password")
        self.assertTrue(EmailOTP.objects.filter(email='duplicate@example.com', purpose=EmailOTP.PURPOSE_PASSWORD_RESET).exists())

    def test_mobile_cards_carousel_present_on_pages(self):
        """Test that product/category collections contain the mobile-cards-carousel class."""
        # 1. Home page
        home_resp = self.client.get(reverse('core:home'))
        self.assertEqual(home_resp.status_code, 200)
        self.assertContains(home_resp, "mobile-cards-carousel")
        self.assertContains(home_resp, "Swipe")

        # 2. Categories page
        cat_resp = self.client.get(reverse('catalog:category_list'))
        self.assertEqual(cat_resp.status_code, 200)
        self.assertContains(cat_resp, "mobile-cards-carousel")

        # 3. Product detail related products
        prod_resp = self.client.get(reverse('catalog:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(prod_resp.status_code, 200)
        # Category switcher has overflow-x-auto
        self.assertContains(cat_resp, "overflow-x-auto")

    def test_admin_permissions_and_crud_lifecycle(self):
        """Test RBAC security and complete CRUD operations for Admin Dashboard."""
        # Setup users
        normal_user = User.objects.create_user(username='customer_jane', password='UserPass123!')
        admin_user = User.objects.create_superuser(username='super_admin', password='AdminPass123!', email='admin@maxview.com')

        # 1. Anonymous Access -> Redirect to Login
        anon_resp = self.client.get(reverse('dashboard:home'))
        self.assertEqual(anon_resp.status_code, 302)
        self.assertIn(reverse('accounts:login'), anon_resp.url)

        anon_crud = self.client.post(reverse('dashboard:product_create'), {'name': 'Illegal Product'})
        self.assertEqual(anon_crud.status_code, 302)

        # 2. Normal Authenticated User Access -> 403 Forbidden
        self.client.login(username='customer_jane', password='UserPass123!')
        forbidden_resp = self.client.get(reverse('dashboard:home'))
        self.assertEqual(forbidden_resp.status_code, 403)

        forbidden_products = self.client.get(reverse('dashboard:products_list'))
        self.assertEqual(forbidden_products.status_code, 403)

        forbidden_post = self.client.post(reverse('dashboard:product_create'), {'name': 'Hacked Product'})
        self.assertEqual(forbidden_post.status_code, 403)

        self.client.logout()

        # 3. Authorized Admin User -> 200 OK & Successful CRUD
        self.client.login(username='super_admin', password='AdminPass123!')

        # Overview
        admin_home = self.client.get(reverse('dashboard:home'))
        self.assertEqual(admin_home.status_code, 200)
        self.assertContains(admin_home, "Executive Control Center")

        # Category CRUD: Create
        cat_create = self.client.post(reverse('dashboard:category_create'), {
            'name': 'Evening Wear',
            'display_order': 5,
            'is_active': True,
        })
        self.assertEqual(cat_create.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Evening Wear').exists())
        new_cat = Category.objects.get(name='Evening Wear')

        # Category CRUD: Update
        cat_update = self.client.post(reverse('dashboard:category_update', kwargs={'pk': new_cat.pk}), {
            'name': 'Haute Evening Wear',
            'display_order': 6,
            'is_active': True,
        })
        self.assertEqual(cat_update.status_code, 302)
        new_cat.refresh_from_db()
        self.assertEqual(new_cat.name, 'Haute Evening Wear')

        # Product CRUD: Create
        prod_create = self.client.post(reverse('dashboard:product_create'), {
            'name': 'Silk Georgette Gown',
            'category': new_cat.pk,
            'sku': 'MV-TEST-GOWN',
            'description': 'A handcrafted silk georgette gown.',
            'price': '899.00',
            'stock_quantity': 15,
            'rating': '5.0',
            'is_active': True,
        })
        self.assertEqual(prod_create.status_code, 302)
        self.assertTrue(Product.objects.filter(sku='MV-TEST-GOWN').exists())
        new_prod = Product.objects.get(sku='MV-TEST-GOWN')

        # Product CRUD: Update
        prod_update = self.client.post(reverse('dashboard:product_update', kwargs={'pk': new_prod.pk}), {
            'name': 'Silk Georgette Gown (Updated)',
            'category': new_cat.pk,
            'sku': 'MV-TEST-GOWN',
            'description': 'Updated description.',
            'price': '999.00',
            'stock_quantity': 20,
            'rating': '4.9',
            'is_active': True,
        })
        self.assertEqual(prod_update.status_code, 302)
        new_prod.refresh_from_db()
        self.assertEqual(new_prod.price, 999.00)

        # Product CRUD: Delete
        prod_delete = self.client.post(reverse('dashboard:product_delete', kwargs={'pk': new_prod.pk}))
        self.assertEqual(prod_delete.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=new_prod.pk).exists())

        # Category CRUD: Delete
        cat_delete = self.client.post(reverse('dashboard:category_delete', kwargs={'pk': new_cat.pk}))
        self.assertEqual(cat_delete.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=new_cat.pk).exists())

        # User Management: Toggle Status & Delete Customer
        toggle_resp = self.client.post(reverse('dashboard:customer_toggle_status', kwargs={'pk': normal_user.pk}))
        self.assertEqual(toggle_resp.status_code, 302)
        normal_user.refresh_from_db()
        self.assertFalse(normal_user.is_active)

        cust_del = self.client.post(reverse('dashboard:customer_delete', kwargs={'pk': normal_user.pk}))
        self.assertEqual(cust_del.status_code, 302)
        self.assertFalse(User.objects.filter(pk=normal_user.pk).exists())




