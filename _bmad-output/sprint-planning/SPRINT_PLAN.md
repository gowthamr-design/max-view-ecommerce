# Sprint Implementation Plan
## MAX VIEW — Luxury Fashion E-Commerce Platform

---

### Document Metadata
- **Project Name:** MAX VIEW Luxury Fashion E-Commerce
- **Document Version:** 1.0.0
- **Document Status:** Approved for Implementation
- **Sprint Cycle:** Sprint 1 through Sprint 4 (Execution Plan)
- **Author:** BMad Sprint Planning Team
- **Stakeholder:** GT
- **Date:** October 14, 2026
- **Location:** `_bmad-output/sprint-planning/SPRINT_PLAN.md`
- **Machine-Readable Tracking:** [`_bmad-output/implementation-artifacts/sprint-status.yaml`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/implementation-artifacts/sprint-status.yaml)

---

## 1. Implementation Readiness Gate Verdict

- **Readiness Gate Result:** **`PASS`**
- **Evaluation Criteria Assessed:**
  1. *PRD Complete & Approved:* All functional requirements (FR-1 through FR-8), user roles, constraints, and non-functional requirements (NFR-1 through NFR-4) are documented in [`_bmad-output/prds/PRD.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/prds/PRD.md).
  2. *Architecture Invariants Established:* Django MVT structure, MySQL schema, session cart engine, Tailwind pipeline, and Vanilla JS interactions are codified in [`_bmad-output/architecture/ARCHITECTURE.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/architecture/ARCHITECTURE.md).
  3. *Database Schema Fully Normalized:* Exact tables, foreign keys, indexes, and fixture plans are defined in [`_bmad-output/database/DATABASE_DESIGN.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/database/DATABASE_DESIGN.md).
  4. *Epics & Stories Granularly Defined:* 8 Epics and 24 Stories with Gherkin acceptance criteria exist in [`_bmad-output/user-stories/epics.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/user-stories/epics.md).
  5. *Orphan / Conflict Check:* 0 orphaned requirements, 0 forward dependency deadlocks.

---

## 2. Sprint Phasing Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 1: Foundation, Styling Pipeline & Catalog Infrastructure             │
│   - Django Setup, MySQL connection, .env isolation (Story 1.1)              │
│   - Tailwind CSS compiler & luxury color tokens (Story 1.2)                 │
│   - Master layout (base.html, navbar, mobile menu) (Story 1.3)              │
│   - Footer & Benefits Showcase Grid (Story 1.4)                             │
│   - Catalog Models (Category, Product, Lookbook) & Migrations (Story 2.1)   │
│   - Django Admin & Seed Data Fixtures (Story 2.2)                           │
│   - Reusable Product Card Component with Rating Stars (Story 2.3)           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ SPRINT 2: Merchandising, Category Discovery & Search                        │
│   - Home Page Hero Section with Dual Images & Sale Badge (Story 3.1)        │
│   - Trending Arrivals Grid (4 Curated Cards) (Story 3.2)                    │
│   - Site Configuration Context Processor (Story 3.3)                        │
│   - Category Browsing View & Strict Category Isolation (Story 4.1)          │
│   - Horizontal Lookbook Image Slider with Touch Gestures (Story 4.2)        │
│   - Keyword Search Engine & Results Page (Story 5.1)                         │
│   - Empty Search State & Recovery Navigation (Story 5.2)                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ SPRINT 3: Shopping Cart Lifecycle & Mock Checkout                           │
│   - Session Cart Engine & Add-to-Cart Action (Story 6.1)                    │
│   - Cart Detail View, Quantity Stepper, Server Subtotals (Story 6.2)        │
│   - Cart Item Removal & Dynamic Navbar Badge (Story 6.3)                    │
│   - Mock Checkout Preview & Order Summary View (Story 6.4)                  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ SPRINT 4: Customer Authentication, Brand Pages & Quality Assurance          │
│   - Customer Registration & Password Hashing (Story 7.1)                    │
│   - Customer Login, Logout & Navbar State Toggle (Story 7.2)                │
│   - Cart Synchronization upon Authentication (Story 7.3)                    │
│   - About Us Page with Brand Heritage Narrative (Story 8.1)                 │
│   - Contact Us Page & Configurable Careers Anchor (Story 8.2)               │
│   - Contact Ingestion Form with CSRF & MySQL Storage (Story 8.3)            │
│   - Newsletter Subscription Ingestion & Validation (Story 8.4)              │
│   - End-to-End Regression, Responsive & Security Audit                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Sprint Plan: Tasks, Dependencies, Criteria & Tests

---

### Sprint 1: Foundation, Styling Pipeline & Catalog Infrastructure
**Focus:** Establish the runtime environment, database connectivity, design system, reusable page layouts, and catalog models.

#### Story 1.1: Django Project Initialization, MySQL Database Configuration, and Environment Isolation
- **Dependencies:** None (Baseline starter).
- **Implementation Tasks:**
  1. Initialize Python virtual environment and install dependencies (`django`, `mysqlclient`, `python-dotenv`, `pillow`).
  2. Create Django project `maxview` and root directory layout.
  3. Create `.env` and `.env.example` defining `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
  4. Configure `maxview/settings/` with MySQL connection parameters and UTF8mb4 options.
  5. Create `apps/` directory and initialize `core`, `catalog`, `cart`, `accounts`.
- **Completion Criteria:** `python manage.py check` executes with 0 errors; database handshake with MySQL succeeds.
- **Testing Tasks:**
  - Verify `python manage.py migrate` creates core Django tables in MySQL.
  - Test missing `.env` variable fallback handling.

#### Story 1.2: Tailwind CSS Pipeline & Luxury Design System Token Configuration
- **Dependencies:** Story 1.1.
- **Implementation Tasks:**
  1. Initialize Tailwind CLI configuration (`tailwind.config.js`).
  2. Inject custom luxury palette: `#171717` (black), `#262626` (charcoal), `#D9A441` (gold), `#FFF4DC` (cream), `#FFFFFF` (white), `#F7F5F0` (neutral).
  3. Configure Google Fonts (Playfair Display & Plus Jakarta Sans).
  4. Create `static/src/input.css` and compile to `static/css/styles.css`.
  5. Configure Django static files settings (`STATICFILES_DIRS`, `STATIC_ROOT`, `STATIC_URL`).
- **Completion Criteria:** Compiled `styles.css` is generated; luxury utility classes resolve properly.
- **Testing Tasks:**
  - Run build script; verify generated CSS contains custom hexadecimal tokens.
  - Verify static file collection via `python manage.py collectstatic --noinput`.

#### Story 1.3: Master Base Template, Responsive Navigation Bar, and Mobile Drawer
- **Dependencies:** Stories 1.1, 1.2.
- **Implementation Tasks:**
  1. Build `templates/base.html` with viewport meta, font links, and Tailwind stylesheet link.
  2. Create `templates/components/navbar.html` with MAX VIEW logo, navigation links, search input, auth icon, and cart badge.
  3. Build mobile slide-out navigation drawer in `navbar.html`.
  4. Author `static/js/main.js` to manage mobile hamburger menu toggling and backdrop dismiss.
- **Completion Criteria:** Navbar renders across all views; mobile drawer toggles cleanly below 768px without horizontal page scroll.
- **Testing Tasks:**
  - Test desktop menu link URLs.
  - Emulate viewport at 375px (iPhone) and verify hamburger open/close animation.

#### Story 1.4: 4-Column Luxury Footer and Benefits Showcase Grid
- **Dependencies:** Stories 1.2, 1.3.
- **Implementation Tasks:**
  1. Build `templates/components/footer.html` with 4 columns: Brand info, Shop links, Support links, and Newsletter capture.
  2. Implement `templates/components/benefits_grid.html` exhibiting the 4 pillars (Free Shipping, Easy Returns, Secure Payment, 24/7 Support) with clean SVG icons.
  3. Include footer and benefits grid in `templates/base.html`.
- **Completion Criteria:** Footer renders at the bottom of all pages with copyright `© 2026 MAX VIEW — All Rights Reserved.`.
- **Testing Tasks:**
  - Verify responsive column reflow from 1-column (mobile) to 4-column (desktop).
  - Verify all static footer anchor links point to valid endpoints.

#### Story 2.1: Catalog Models & MySQL Migrations
- **Dependencies:** Story 1.1.
- **Implementation Tasks:**
  1. Define `Category` model in `apps/catalog/models.py` (`name`, `slug`, `description`, `image`, `display_order`, `is_active`).
  2. Define `Product` model (`category` FK with `PROTECT`, `name`, `slug`, `sku`, `price`, `rating`, `stock_quantity`, `is_trending`, `image`, `is_active`).
  3. Define `ProductImage` model for secondary gallery images (`product` FK with `CASCADE`).
  4. Define `LookbookSlide` model (`title`, `subtitle`, `image`, `category` FK with `SET_NULL`, `display_order`).
  5. Add composite database indexes (`idx_cat_active`, `idx_trending_active`).
  6. Generate and apply migrations.
- **Completion Criteria:** MySQL schema reflects all 4 tables with correct foreign keys, nullability, and indexes.
- **Testing Tasks:**
  - Execute `python manage.py makemigrations catalog` and `migrate`.
  - Verify tables exist in MySQL via database inspection.

#### Story 2.2: Django Admin Integration & Initial Catalog Data Fixtures Seeding
- **Dependencies:** Story 2.1.
- **Implementation Tasks:**
  1. Register `CategoryAdmin`, `ProductAdmin`, and `LookbookSlideAdmin` in `apps/catalog/admin.py`.
  2. Add `ProductImageInline` to `ProductAdmin`.
  3. Create fixture `initial_catalog.json` with 4 categories (*Men's Wear*, *Women's Wear*, *Kids' Wear*, *Accessories*) and 4 initial products (Men's ₹499, Women's ₹599, Kids' ₹499, Accessories ₹899).
  4. Seed initial lookbook slide records.
- **Completion Criteria:** Initial sample catalog loads into MySQL via `loaddata` and is viewable in Django Admin.
- **Testing Tasks:**
  - Execute `python manage.py loaddata initial_catalog.json`.
  - Log into `/admin/` and verify categories and products are editable.

#### Story 2.3: Reusable Product Card Component with Gold Star Ratings & Hover Animations
- **Dependencies:** Stories 1.2, 2.1.
- **Implementation Tasks:**
  1. Create `templates/components/product_card.html`.
  2. Render uniform product image with overflow hidden and `scale-105` hover zoom.
  3. Display category badge, product title, description snippet, and formatted price (`₹499.00`).
  4. Render 5 gold star icons (`#D9A441`) representing the product's decimal rating.
  5. Add "Add to Cart" button with CSRF token and product ID attribute.
- **Completion Criteria:** Product card renders identically across Home and Category pages without layout shifts.
- **Testing Tasks:**
  - Test hover transition smoothness.
  - Test card rendering with long product descriptions to ensure text truncation works.

---

### Sprint 2: Merchandising, Category Discovery & Search
**Focus:** Build the complete Home page, Category catalog page with interactive lookbook slider, and search system.

#### Story 3.1: Home Page Hero Section with Dual Imagery & Sale Badge
- **Dependencies:** Stories 1.3, 1.4, 2.2.
- **Implementation Tasks:**
  1. Create `apps/core/views.py::HomeView` (TemplateView).
  2. Build `templates/core/home.html` extending `base.html`.
  3. Construct luxury hero layout: Left side brand headline, description (*"Premium fashion bringing modern trends with uncompromising quality and style."*), and "Shop Now" button.
  4. Right side dual visual layout with primary fashion hero image, secondary inset image, and gold sale offer badge.
  5. Add smooth scroll anchor to "Explore Details".
- **Completion Criteria:** Visiting `/` loads the complete luxury hero with working CTAs.
- **Testing Tasks:**
  - Click "Shop Now"; verify it navigates to `/shop/categories/`.
  - Verify layout responsiveness across 375px, 768px, and 1280px.

#### Story 3.2: Trending Arrivals Showcase Grid Integration
- **Dependencies:** Stories 2.3, 3.1.
- **Implementation Tasks:**
  1. Update `HomeView.get_context_data` to query `Product.objects.filter(is_trending=True, is_active=True)[:4]`.
  2. Embed product cards into `templates/core/home.html` in a responsive 4-column grid.
  3. Pass seeded items (Men's, Women's, Kids', Accessories) to the template.
- **Completion Criteria:** 4 distinct trending products render on the Home page with ratings and prices in INR.
- **Testing Tasks:**
  - Verify exactly 4 cards render.
  - Inspect SQL queries to confirm `select_related('category')` prevents N+1 queries.

#### Story 3.3: Global Site Configuration Context Processor
- **Dependencies:** Story 1.1.
- **Implementation Tasks:**
  1. Create `SiteConfig` model in `apps/core/models.py`.
  2. Create context processor `apps/core/context_processors.py::site_settings`.
  3. Register in `settings.py` under `TEMPLATES['OPTIONS']['context_processors']`.
  4. Seed singleton configuration record with Tirupur address, support phone, and support email.
- **Completion Criteria:** `{{ site_config.store_address }}` and contact details render in navbar/footer automatically.
- **Testing Tasks:**
  - Modify address in Django Admin; verify change appears on frontend without restarting server.

#### Story 4.1: Category Browsing View & Strict Category Isolation Filtering
- **Dependencies:** Stories 2.1, 2.2, 2.3.
- **Implementation Tasks:**
  1. Create `apps/catalog/views.py::CategoryListView` and `CategoryDetailView`.
  2. Map URL routes: `/shop/categories/` and `/shop/category/<slug:slug>/`.
  3. Render category navigation pills/tabs for *Men's Wear*, *Women's Wear*, *Kids' Wear*, *Accessories*.
  4. Filter product queryset strictly by `category__slug=slug`.
  5. Render empty state notice when a category contains no active products.
- **Completion Criteria:** Selecting a category shows strictly that category's items with zero leakage from other categories.
- **Testing Tasks:**
  - Test filtering for Men's Wear; confirm Women's/Kids'/Accessories products are not in the DOM.
  - Test invalid category slug; confirm HTTP 404 response.

#### Story 4.2: Horizontal Lookbook Image Slider with Prev/Next Controls & Touch Swipe
- **Dependencies:** Stories 1.2, 4.1.
- **Implementation Tasks:**
  1. Create `templates/components/slider.html` embedding lookbook slide models.
  2. Author `static/js/slider.js` handling carousel translation.
  3. Add Next (`>`) and Previous (`<`) button click listeners.
  4. Add mobile touch event listeners (`touchstart`, `touchmove`, `touchend`) to calculate swipe delta.
  5. Apply CSS `transform: translateX(...)` with smooth transitions.
- **Completion Criteria:** Slider shifts smoothly across slides; supports touch swiping on mobile devices without layout overflow.
- **Testing Tasks:**
  - Click next/prev buttons on desktop; verify active slide indexes.
  - Emulate touch swipe on Chrome DevTools mobile view; confirm translation occurs.

#### Story 5.1: Global Keyword Search Processing & Results View
- **Dependencies:** Stories 2.1, 2.3.
- **Implementation Tasks:**
  1. Create `apps/core/views.py::SearchView` querying `q` parameter.
  2. Implement search query logic using `Q(name__icontains=q) | Q(description__icontains=q)`.
  3. Create `templates/core/search_results.html` rendering matching product grid.
  4. Connect navbar search form with GET action to `/search/`.
- **Completion Criteria:** Entering keyword (e.g. "Linen") returns all matching products and displays total count.
- **Testing Tasks:**
  - Search for "Shirt"; verify matching items appear.
  - Test search input with HTML/JS characters (`<script>`); verify automatic escaping.

#### Story 5.2: Empty Search State & Catalog Return Navigation
- **Dependencies:** Story 5.1.
- **Implementation Tasks:**
  1. Add zero-match conditional block in `templates/core/search_results.html`.
  2. Render message *"No products found matching '<query>'"*.
  3. Provide prominent CTA button *"Explore All Categories"* routing to `/shop/categories/`.
- **Completion Criteria:** Empty searches present clear recovery UI without dead ends.
- **Testing Tasks:**
  - Search for non-existent term "nonexistentproduct999"; verify zero-state displays with recovery button.

---

### Sprint 3: Shopping Cart Lifecycle & Mock Checkout
**Focus:** Build the complete shopping cart engine, line-item quantity stepper, price recalculation, and mock checkout flow.

#### Story 6.1: Session-Based Shopping Cart Engine & Add-to-Cart Action
- **Dependencies:** Stories 2.1, 2.3.
- **Implementation Tasks:**
  1. Author `apps/cart/cart.py::SessionCart` class managing `request.session['cart']`.
  2. Create `CartAddView` in `apps/cart/views.py` handling POST requests.
  3. Validate product ID and stock availability.
  4. Add item to session cart dictionary: `{product_id: {'quantity': qty, 'price': str(product.price)}}`.
  5. Return JSON or redirect with flash notification.
- **Completion Criteria:** Clicking "Add to Cart" adds item to session and increments item count.
- **Testing Tasks:**
  - POST to `/cart/add/<id>/`; verify session contains product ID and quantity.
  - Attempt to add out-of-stock item; verify rejection.

#### Story 6.2: Cart Detail View, Quantity Stepper, and Server-Side Subtotal Recalculation
- **Dependencies:** Story 6.1.
- **Implementation Tasks:**
  1. Create `CartDetailView` rendering `templates/cart/cart_detail.html`.
  2. Query active `Product` models to fetch fresh database prices for all session items.
  3. Implement `CartUpdateView` accepting updated quantity values.
  4. Calculate item subtotals and grand total strictly on server side.
  5. Check free shipping eligibility (subtotal >= ₹999.00).
- **Completion Criteria:** Cart items display accurate prices, subtotals, shipping fee, and grand total in INR.
- **Testing Tasks:**
  - Modify quantity from 1 to 3; verify item subtotal triples and grand total updates.
  - Submit tampered price parameter in request; verify server overrides with database price.

#### Story 6.3: Cart Item Removal & Dynamic Navbar Badge Updates
- **Dependencies:** Stories 6.1, 6.2.
- **Implementation Tasks:**
  1. Create `CartRemoveView` deleting item key from session dictionary.
  2. Create context processor `apps/cart/context_processors.py::cart_summary`.
  3. Register context processor in `settings.py` to inject `cart_total_items` and `cart_grand_total`.
  4. Bind navbar cart icon badge to `cart_total_items`.
  5. Add empty state to `cart_detail.html` with "Continue Shopping" link.
- **Completion Criteria:** Removing an item deletes it immediately, updates totals, and decrements navbar badge.
- **Testing Tasks:**
  - Remove an item; confirm it disappears from cart and badge decrements.
  - Empty cart completely; verify empty state message renders.

#### Story 6.4: Mock Checkout Preview & Order Summary View
- **Dependencies:** Stories 6.2, 6.3.
- **Implementation Tasks:**
  1. Create `CheckoutReviewView` rendering `templates/cart/checkout_review.html`.
  2. Display read-only order summary breakdown (items, quantities, subtotal, shipping, grand total).
  3. Render mock shipping address and customer details form.
  4. Add "Place Order (Mock Demo)" button that clears session cart and redirects to a success screen with order reference ID.
- **Completion Criteria:** Shoppers can complete a full demonstration checkout without invoking real payment gateways.
- **Testing Tasks:**
  - Complete mock checkout; verify success message displays and cart is emptied.
  - Attempt to access checkout with empty cart; confirm redirection to cart page.

---

### Sprint 4: Customer Authentication, Brand Pages & Quality Assurance
**Focus:** Build customer authentication, session cart merge, brand/contact pages, newsletter capture, and run final end-to-end verification.

#### Story 7.1: User Registration with Validation & Password Policy
- **Dependencies:** Story 1.1.
- **Implementation Tasks:**
  1. Author `RegistrationForm` in `apps/accounts/forms.py` (Full Name, Email, Username, Password, Confirm Password).
  2. Enforce standard Django password validation rules.
  3. Create `UserRegistrationView` in `apps/accounts/views.py`.
  4. Create `templates/accounts/register.html` with Tailwind luxury styling.
  5. Create `CustomerProfile` record linked to new `User`.
- **Completion Criteria:** New users can register successfully; passwords stored using PBKDF2 hashing.
- **Testing Tasks:**
  - Submit form with mismatched passwords; verify validation error.
  - Submit valid registration; verify user row exists in MySQL `auth_user`.

#### Story 7.2: Customer Login, Logout & Navbar Authentication State Toggle
- **Dependencies:** Story 7.1.
- **Implementation Tasks:**
  1. Create `UserLoginView` and `UserLogoutView` in `apps/accounts/views.py`.
  2. Build `templates/accounts/login.html`.
  3. Update `navbar.html` to conditionally display user username/profile icon and "Logout" link when `user.is_authenticated`.
  4. Redirect user to home page with confirmation toast upon login and logout.
- **Completion Criteria:** Login authenticates user and updates navbar; logout securely clears session.
- **Testing Tasks:**
  - Log in with valid credentials; verify navbar reflects logged-in state.
  - Log out; verify navbar displays "Login" link.

#### Story 7.3: Cart Synchronization upon Customer Authentication
- **Dependencies:** Stories 6.1, 7.2.
- **Implementation Tasks:**
  1. Define `Cart` and `CartItem` models in `apps/cart/models.py`.
  2. Create service function `merge_session_cart_to_db(user, request)`.
  3. Hook merge service into `UserLoginView.form_valid`.
  4. Transfer items from session dictionary into database `CartItem` rows.
- **Completion Criteria:** Items added as an anonymous guest persist into customer's account after logging in.
- **Testing Tasks:**
  - Add item to cart as guest, log in, navigate to cart; verify item is still present.

#### Story 8.1: About Us Page Layout & Brand Heritage Presentation
- **Dependencies:** Stories 1.3, 1.4.
- **Implementation Tasks:**
  1. Create `AboutView` in `apps/core/views.py`.
  2. Build `templates/core/about.html`.
  3. Present official brand heritage story and mission statement with elegant editorial typography.
  4. Include high-resolution fashion visual with subtle zoom effect.
- **Completion Criteria:** `/about/` displays brand narrative with consistent luxury palette and zero broken styling.
- **Testing Tasks:**
  - Verify copy matches approved PRD text.
  - Test responsive layout on mobile and desktop.

#### Story 8.2: Contact Us Page with Business Information & Configurable Careers Anchor
- **Dependencies:** Stories 1.3, 3.3.
- **Implementation Tasks:**
  1. Create `ContactView` in `apps/core/views.py`.
  2. Build `templates/core/contact.html`.
  3. Display verified store coordinates (Tirupur address, phone, email) pulled from `SiteConfig`.
  4. Add Careers section *"Careers at MAX VIEW"* with description and *"Explore Jobs"* action.
- **Completion Criteria:** Contact coordinates and careers blurb render clearly.
- **Testing Tasks:**
  - Verify phone and email link actions (`tel:` and `mailto:`).
  - Verify Careers button destination functions without errors.

#### Story 8.3: Contact Ingestion Form with CSRF Protection & MySQL Storage
- **Dependencies:** Stories 1.1, 8.2.
- **Implementation Tasks:**
  1. Create `ContactMessage` model in `apps/core/models.py`.
  2. Create `ContactForm` in `apps/core/forms.py` with validation.
  3. Handle form POST in `ContactView` with CSRF protection and `@transaction.atomic`.
  4. Save submissions to MySQL and display success notification.
- **Completion Criteria:** Valid inquiries are persisted to MySQL; invalid submissions display inline field errors.
- **Testing Tasks:**
  - Submit empty form; verify required field errors.
  - Submit valid message; verify record is created in `core_contactmessage`.

#### Story 8.4: Newsletter Subscription Ingestion & Client/Server Validation
- **Dependencies:** Stories 1.1, 1.4.
- **Implementation Tasks:**
  1. Create `NewsletterSubscriber` model in `apps/core/models.py`.
  2. Create `NewsletterSubscribeView` handling POST requests.
  3. Validate email format; handle duplicates gracefully.
  4. Save subscriber in MySQL and return feedback toast.
- **Completion Criteria:** Newsletter submissions from the footer are validated and saved in MySQL.
- **Testing Tasks:**
  - Submit valid email; verify entry in `core_newslettersubscriber`.
  - Submit invalid email; verify validation rejection.

---

## 4. Verification & Testing Strategy

| Verification Dimension | Protocol | Acceptance Target |
| :--- | :--- | :--- |
| **Route Coverage** | Execute automated GET requests to all defined URLs. | 100% 200 OK responses (no 404s, no 500s). |
| **Responsive UI** | Inspect viewports at 375px, 768px, 1024px, 1440px. | Zero horizontal overflow; touch targets >= 44x44px. |
| **Database Integrity** | Inspect MySQL tables and foreign key constraints. | Normalized schema; foreign key cascades intact. |
| **Security Audit** | Verify CSRF tokens on forms; verify PBKDF2 password hashes. | 0 CSRF omissions; 0 plaintext credentials. |
| **Cart Mathematics** | Add items with various quantities; test subtotal thresholds. | Exact ₹ rounding; free shipping threshold at ₹999. |

---

## 5. Next Steps

1. **Review & Approval:** Stakeholder (GT) reviews and approves this Sprint Implementation Plan.
2. **Transition to Implementation:** Engage **Amelia (`/bmad-agent-dev`)** to initiate **Sprint 1 (Story 1.1: Django Project Initialization & MySQL Setup)**.
