# Technical Architecture Document
## MAX VIEW — Luxury Fashion E-Commerce Platform

---

### Document Metadata
- **Project Name:** MAX VIEW Luxury Fashion E-Commerce
- **Document Version:** 1.0.0
- **Document Status:** Draft for Review
- **Author:** Winston, System Architect (BMad Method)
- **Stakeholder:** GT
- **Date:** October 14, 2026
- **Location:** `_bmad-output/architecture/ARCHITECTURE.md`
- **Companion Document:** [`_bmad-output/database/DATABASE_DESIGN.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/database/DATABASE_DESIGN.md)

---

## 1. Architectural Principles & Paradigm

### 1.1 Core Architectural Paradigm
The MAX VIEW platform adopts a **Monolithic Server-Side Rendered (SSR) Model-View-Template (MVT)** architecture built on Python Django.

```
       Browser (Client)
   [HTML + Tailwind CSS + JS]
             │   ▲
  HTTP(S) Req│   │ SSR HTML Response
             ▼   │
   ┌────────────────────────────────────────┐
   │ Nginx (Reverse Proxy & Static Cache)   │
   └───────────────────┬────────────────────┘
                       │ WSGI
   ┌───────────────────▼────────────────────┐
   │ Gunicorn WSGI HTTP Server              │
   └───────────────────┬────────────────────┘
                       │
   ┌───────────────────▼────────────────────┐
   │ Django Web Application Core            │
   │  ├── Security Middleware & Sessions    │
   │  ├── App Routing (URLconf)             │
   │  ├── Context Processors (Cart, Config) │
   │  ├── Views (Class-Based Views)         │
   │  └── Django Templates & Partials       │
   └───────────────────┬────────────────────┘
                       │ Django ORM
   ┌───────────────────▼────────────────────┐
   │ MySQL 8.0 Relational Database (InnoDB) │
   └────────────────────────────────────────┘
```

### 1.2 Guiding Architectural Decisions (AD)
- **AD-1 [Monolithic Django SSR]:** Deliver server-rendered HTML using Django's template engine. Prevents client-side hydration delays, ensures immediate search indexing, and keeps development streamlined without Node/SPA runtime dependencies.
- **AD-2 [Relational MySQL Database]:** Use MySQL 8.0 with the InnoDB storage engine for ACID transactions, foreign key constraints, and normalized data integrity.
- **AD-3 [Hybrid Session-Persistent Cart]:** Maintain active shopping carts in Django session cookies for anonymous shoppers, syncing atomically with database cart records upon user authentication. Server enforces canonical price calculation against the database at all times.
- **AD-4 [Standalone Tailwind Asset Pipeline]:** Compile utility CSS using the standalone Tailwind CLI into static production stylesheets with zero runtime JS framework overhead.
- **AD-5 [Unobtrusive Vanilla JavaScript]:** Restrict client-side JavaScript to isolated ES6 micro-modules (image slider touch gestures, dynamic quantity recalculations, modal handling, mobile navigation toggle) without heavy reactive libraries.

---

## 2. Project Directory & Folder Structure

The application follows an enterprise Django modular structure under an `apps/` namespace:

```
c:\Users\91995\OneDrive\Documents\Ecom website\
├── manage.py
├── requirements.txt
├── .env.example
├── .env                                  # Git-ignored local configuration
├── tailwind.config.js                    # Tailwind theme tokens & content scanners
│
├── maxview/                              # Root configuration module
│   ├── __init__.py
│   ├── asgi.py                           # ASGI interface
│   ├── wsgi.py                           # Production WSGI interface
│   ├── urls.py                           # Root URLconf aggregating apps
│   └── settings/
│       ├── __init__.py
│       ├── base.py                       # Shared settings (Apps, Middleware, Templates)
│       ├── development.py                # Local debug settings
│       └── production.py                 # Production hardening & SSL settings
│
├── apps/                                 # Domain-driven Django applications
│   ├── core/                             # General pages, static information, messaging
│   │   ├── migrations/
│   │   ├── forms.py                      # ContactForm, NewsletterSubscriptionForm
│   │   ├── models.py                     # ContactMessage, NewsletterSubscriber, SiteConfig
│   │   ├── views.py                      # HomeView, AboutView, ContactView, SearchView
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── catalog/                          # Products, Categories, Collections, Slider
│   │   ├── migrations/
│   │   ├── models.py                     # Category, Product, ProductImage, LookbookSlide
│   │   ├── views.py                      # CategoryListView, ProductDetailView
│   │   ├── urls.py
│   │   ├── services.py                   # Catalog query optimization & filters
│   │   └── admin.py                      # Product inline image management
│   │
│   ├── cart/                             # Session & DB Cart calculations
│   │   ├── migrations/
│   │   ├── models.py                     # Cart, CartItem
│   │   ├── cart.py                       # SessionCart management service
│   │   ├── views.py                      # CartDetailView, CartAddView, CartUpdateView, CartRemoveView, CheckoutReviewView
│   │   ├── urls.py
│   │   └── context_processors.py         # Injects cart item counter & subtotal into all templates
│   │
│   └── accounts/                         # Customer authentication & profile
│       ├── migrations/
│       ├── forms.py                      # RegistrationForm, LoginForm, ProfileUpdateForm
│       ├── models.py                     # CustomerProfile
│       ├── views.py                      # RegisterView, LoginView, LogoutView, ProfileView
│       ├── urls.py
│       └── admin.py
│
├── static/                               # Static assets
│   ├── src/
│   │   └── input.css                     # Tailwind source file with custom components
│   ├── css/
│   │   └── styles.css                    # Compiled production Tailwind CSS
│   ├── js/
│   │   ├── main.js                       # Mobile drawer, alert auto-dismiss, CSRF setup
│   │   ├── slider.js                     # Lookbook touch-swipe and navigation controls
│   │   └── cart.js                       # Asynchronous add-to-cart & quantity stepper
│   └── images/                           # Static brand logos, fallback placeholders
│
├── media/                                # User/Admin uploaded media assets
│   ├── products/                         # Catalog product photography
│   ├── categories/                       # Category banner visuals
│   └── lookbook/                         # High-res slider visuals
│
├── templates/                            # Centralized Django HTML templates
│   ├── base.html                         # Master layout template
│   ├── components/
│   │   ├── navbar.html                   # Responsive luxury navigation bar
│   │   ├── footer.html                   # 4-column luxury footer & newsletter
│   │   ├── product_card.html             # Standard product display card
│   │   ├── benefits_grid.html            # 4-pillar benefits showcase
│   │   ├── slider.html                   # Lookbook horizontal image slider
│   │   └── messages.html                 # Toast / alert notifications
│   ├── core/
│   │   ├── home.html                     # Home page
│   │   ├── about.html                    # About Us page
│   │   ├── contact.html                  # Contact Us page
│   │   └── search_results.html           # Product search results view
│   ├── catalog/
│   │   ├── category_list.html            # Category browsing & filtered view
│   │   └── product_detail.html           # Dedicated product inspection page
│   ├── cart/
│   │   ├── cart_detail.html              # Interactive cart summary
│   │   └── checkout_review.html          # Order preview (Mock checkout)
│   └── accounts/
│       ├── login.html                    # Customer login
│       ├── register.html                 # Customer registration
│       └── profile.html                  # Customer profile overview
│
└── _bmad-output/                         # Project specifications & governance artifacts
```

---

## 3. Django App Boundaries & Responsibilities

| App Name | Primary Domain Responsibility | Key Models Owned | Primary Views Exposed |
| :--- | :--- | :--- | :--- |
| **`apps.core`** | Brand pages, global search, contact submissions, newsletter, site-wide parameters. | `ContactMessage`, `NewsletterSubscriber`, `SiteConfig` | `HomeView`, `AboutView`, `ContactView`, `SearchView`, `NewsletterSubscribeView` |
| **`apps.catalog`** | Product catalog hierarchy, stock status, lookbook slides, category filtering. | `Category`, `Product`, `ProductImage`, `LookbookSlide` | `CategoryListView`, `CategoryDetailView`, `ProductDetailView` |
| **`apps.cart`** | Session-based & DB cart lifecycle, item quantities, server-side price validation. | `Cart`, `CartItem` | `CartDetailView`, `CartAddView`, `CartUpdateView`, `CartRemoveView`, `CheckoutReviewView` |
| **`apps.accounts`** | User authentication, session management, customer profile data. | `CustomerProfile` (extending Django `User`) | `UserRegistrationView`, `UserLoginView`, `UserLogoutView`, `CustomerProfileView` |

---

## 4. URL Routing Scheme

### 4.1 Master Routing (`maxview/urls.py`)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('shop/', include('apps.catalog.urls', namespace='catalog')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 4.2 Endpoint Specifications

| Application | Pattern | View Function / Class | Name | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **core** | `/` | `HomeView` | `core:home` | Renders Home, Hero, Trending, Benefits |
| **core** | `/about/` | `AboutView` | `core:about` | Renders About Us & Brand Story |
| **core** | `/contact/` | `ContactView` | `core:contact` | Renders Contact details & handles form POST |
| **core** | `/search/` | `SearchView` | `core:search` | Query-filtered product search |
| **core** | `/newsletter/subscribe/` | `NewsletterSubscribeView` | `core:newsletter_subscribe` | Ingests newsletter email POST |
| **catalog** | `/categories/` | `CategoryListView` | `catalog:category_list` | Displays categories & slider showcase |
| **catalog** | `/category/<slug:slug>/` | `CategoryDetailView` | `catalog:category_detail` | Displays products for specific category |
| **catalog** | `/product/<slug:slug>/` | `ProductDetailView` | `catalog:product_detail` | Displays single product detail view |
| **cart** | `/cart/` | `CartDetailView` | `cart:detail` | Renders cart items & total breakdown |
| **cart** | `/cart/add/<int:product_id>/` | `CartAddView` | `cart:add` | Adds item with specified quantity |
| **cart** | `/cart/update/<int:product_id>/`| `CartUpdateView` | `cart:update` | Modifies line-item quantity |
| **cart** | `/cart/remove/<int:product_id>/`| `CartRemoveView` | `cart:remove` | Removes product from active cart |
| **cart** | `/cart/checkout/` | `CheckoutReviewView` | `cart:checkout` | Displays mock checkout preview |
| **accounts** | `/accounts/login/` | `UserLoginView` | `accounts:login` | Authenticates existing user |
| **accounts** | `/accounts/register/` | `UserRegistrationView`| `accounts:register` | Registers new user account |
| **accounts** | `/accounts/logout/` | `UserLogoutView` | `accounts:logout` | Terminates session securely |

---

## 5. View Layer & Context Architecture

### 5.1 View Architecture Paradigm
- **Class-Based Views (CBVs):** Standardized on Django generic CBVs (`TemplateView`, `ListView`, `DetailView`, `FormView`) for structured, readable lifecycle handling.
- **Atomic Transactional Endpoints:** All mutation views (Cart Add/Update/Remove, Contact Post, User Registration) wrapped in `@transaction.atomic` to prevent partial state corruption.
- **Graceful Error Handling:** Form invalidation triggers structured template re-rendering with field-specific errors, without losing user input.

### 5.2 Context Processors
To avoid duplicating shared header and footer data across every view, custom context processors are injected globally via `TEMPLATES['OPTIONS']['context_processors']`:
1. `apps.cart.context_processors.cart_summary`:
   - Computes total cart item quantity (`cart_total_items`) for the navbar badge.
   - Computes cart grand total (`cart_grand_total`).
2. `apps.core.context_processors.site_settings`:
   - Exposes global store parameters (e.g., `STORE_ADDRESS`, `SUPPORT_PHONE`, `SUPPORT_EMAIL`, `FREE_SHIPPING_THRESHOLD`).
3. `apps.catalog.context_processors.navigation_categories`:
   - Exposes the active categories list (`nav_categories`) for the navbar dropdown/links.

---

## 6. Cart Architecture & Lifecycle

```
                     ┌───────────────────────────────┐
                     │ Shopper Adds Product to Cart  │
                     └───────────────┬───────────────┘
                                     │
                     ┌───────────────▼───────────────┐
                     │ Check User Authentication     │
                     └───────┬───────────────┬───────┘
            Anonymous        │               │ Authenticated
       ┌─────────────────────┘               └─────────────────────┐
       ▼                                                           ▼
┌──────────────────────────────┐              ┌─────────────────────────────────┐
│ SessionCart Engine           │              │ Database Cart Engine            │
│  - Stored in request.session │              │  - Cart linked to User (FK)     │
│  - Serialized dictionary:    │              │  - CartItem records in MySQL    │
│    { product_id: {qty, ..} } │              │  - Atomic row locking           │
└──────────────┬───────────────┘              └────────────────┬────────────────┘
               │                                               │
               │      ┌─────────────────────────────────┐      │
               └─────►│ Server-Side Price Verification  │◄─────┘
                      │  - Query active Product.price   │
                      │  - Recalculate Subtotal & Total │
                      │  - Reject client price tampering│
                      └────────────────┬────────────────┘
                                       │
                      ┌────────────────▼────────────────┐
                      │ Return Updated Cart State / HTML│
                      └─────────────────────────────────┘
```

### 6.1 Authentication Cart Reconciliation
When an anonymous shopper who already has items in their `request.session['cart']` logs in:
1. `UserLoginView` signals `apps.cart.services.merge_session_cart_to_db(user, request)`.
2. Existing database cart for `user` is retrieved or created.
3. For each session item:
   - If product exists in database cart, quantity is incremented (capped at available inventory).
   - If product is new to database cart, a new `CartItem` record is created.
4. Session cart dictionary is synchronized to match the consolidated database cart.

---

## 7. Templates & UI Styling Architecture

### 7.1 Template Inheritance Hierarchy
```
templates/base.html
├── components/navbar.html
├── components/messages.html
├── {% block content %}
│   ├── core/home.html (includes components/benefits_grid.html, components/product_card.html)
│   ├── catalog/category_list.html (includes components/slider.html, components/product_card.html)
│   ├── cart/cart_detail.html
│   └── ...
└── components/footer.html
```

### 7.2 Design System Tokens (Tailwind Configuration)
Configured in `tailwind.config.js`:
```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        luxury: {
          black: '#171717',      // Primary dark backgrounds & headers
          charcoal: '#262626',   // Card surfaces & elevated sections
          gold: '#D9A441',       // Champagne gold accents, stars, active badges
          'gold-hover': '#C29135',
          cream: '#FFF4DC',      // Elegant contrast typography & pills
          white: '#FFFFFF',      // High-contrast text & backgrounds
          neutral: '#F7F5F0',    // Soft body backgrounds for clean aesthetic
        }
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

---

## 8. Client-Side JavaScript Architecture

JavaScript is kept lightweight, modular, and dependency-free:
1. **`main.js`**:
   - Manages mobile drawer toggle (`#mobile-menu-btn` and `#mobile-menu`).
   - Auto-dismisses flash message banners after 5 seconds.
   - Configures `csrfSafeMethod` helper for AJAX/fetch requests using standard `X-CSRFToken` header from cookies.
2. **`slider.js`**:
   - Manages the horizontal lookbook carousel on `/categories/`.
   - Supports keyboard arrow navigation, next/prev button clicks, and touch touchstart/touchmove swiping with CSS translation transforms.
3. **`cart.js`**:
   - Asynchronous quantity stepper (`+` and `-`) with real-time DOM update of item subtotals and grand total without full page reloads.

---

## 9. Security Architecture

- **CSRF Defense:** `CsrfViewMiddleware` active globally. All forms inject `{% csrf_token %}`. All fetch requests attach `headers: {'X-CSRFToken': getCookie('csrftoken')}`.
- **SQL Injection Prevention:** 100% adherence to Django ORM parameterized queries. Raw SQL strictly prohibited.
- **Password Security:** Django `PBKDF2PasswordHasher` with SHA256 and minimum 100,000 iterations.
- **XSS Mitigation:** Django template auto-escaping enabled by default. `safe` template tag used only on verified, sanitized content.
- **Session Protection:**
  - `SESSION_COOKIE_HTTPONLY = True` (blocks JavaScript access).
  - `SESSION_COOKIE_AGE = 1209600` (2 weeks default expiration).
  - `SESSION_EXPIRE_AT_BROWSER_CLOSE = False` (cart persistence across browser restarts).
  - `CSRF_COOKIE_HTTPONLY = False` (allows script to read token for Fetch headers; token is non-executable).

---

## 10. Deployment & Environmental Strategy

### 10.1 Environment Variable Isolation (`.env`)
```bash
DEBUG=False
SECRET_KEY=change-me-to-a-high-entropy-random-secret
ALLOWED_HOSTS=maxview.example.com,localhost,127.0.0.1
DB_NAME=maxview_db
DB_USER=maxview_user
DB_PASSWORD=strong_production_password
DB_HOST=127.0.0.1
DB_PORT=3306
STATIC_ROOT=/var/www/maxview/static/
MEDIA_ROOT=/var/www/maxview/media/
```

### 10.2 Production Stack Architecture
- **Web Server:** Nginx acting as reverse proxy, handling SSL termination, and serving static/media files directly with HTTP caching headers.
- **Application Server:** Gunicorn executing 3–4 synchronous worker processes managed via systemd.
- **Database Server:** MySQL 8.0 configured with UTF8mb4 character set.

---

## 11. Approval & Governance

- **Architect:** Winston, System Architect 🏗️
- **Status:** Complete for Review
- **Next Phase:** Database design review (`_bmad-output/database/DATABASE_DESIGN.md`) followed by stakeholder sign-off before code implementation.
