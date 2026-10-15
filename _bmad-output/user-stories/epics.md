---
status: ready_for_review
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-breakdown-stories
inputDocuments:
  - _bmad-output/prds/PRD.md
  - _bmad-output/architecture/ARCHITECTURE.md
  - _bmad-output/database/DATABASE_DESIGN.md
---

# MAX VIEW - Comprehensive Epics and User Stories Breakdown

## Overview

This document specifies the complete epic and user story breakdown for **MAX VIEW Luxury Fashion E-Commerce**. Requirements have been decomposed directly from the approved PRD ([`_bmad-output/prds/PRD.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/prds/PRD.md)), Technical Architecture ([`_bmad-output/architecture/ARCHITECTURE.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/architecture/ARCHITECTURE.md)), and Database Specification ([`_bmad-output/database/DATABASE_DESIGN.md`](file:///c:/Users/91995/OneDrive/Documents/Ecom%20website/_bmad-output/database/DATABASE_DESIGN.md)).

All stories are structured in implementation-ready order, equipped with Gherkin acceptance criteria (Given-When-Then), and span frontend, backend, database migrations, validation, security, and responsive UI design.

---

## Requirements Inventory

### Functional Requirements
- **FR-1:** Global Navigation & Header System (Logo, navigation links, auth status display, search bar, cart indicator with badge, mobile hamburger drawer).
- **FR-2:** Home Page Presentation & Merchandising (Luxury Hero section with dual imagery & sale badge, 4 Trending Arrivals cards, 4-pillar benefits grid, 4-column luxury footer with newsletter capture).
- **FR-3:** Category Hierarchy & Interactive Showcase (4 categories: Men's, Women's, Kids', Accessories; isolated category filtering; horizontal lookbook image slider with prev/next and touch swiping; uniform product cards).
- **FR-4:** Product Search Experience (Keyword query matching across title/description, result grid display, zero-match fallback with catalog return button).
- **FR-5:** Shopping Cart & Order Preparation (Session-based cart for guests, DB sync on authentication, add/update quantity/remove items, server-side price validation, mock checkout preview).
- **FR-6:** Brand Heritage & Contact Systems (About Us page, store contact details in Tirupur, configurable careers exploratory link, CSRF-protected contact message submission).
- **FR-7:** Customer Authentication & Access Control (User registration, secure password hashing, login/logout, authenticated UI states).
- **FR-8:** Database & Administration Model (MySQL 8.0 schema via Django ORM, Django Admin catalog management, initial sample data fixtures).

### Non-Functional Requirements
- **NFR-1 (Performance & Responsiveness):** FCP < 1.5s desktop, < 2.5s mobile; responsive breakpoints (mobile, tablet, desktop); zero horizontal overflow; smooth CSS/JS transitions.
- **NFR-2 (Security & Data Integrity):** 100% CSRF token enforcement; Django ORM parameterization (no raw SQL); secure password hashing (PBKDF2/SHA256); `.env` credential isolation.
- **NFR-3 (Design System Compliance):** Luxury color tokens (`#171717` Black, `#262626` Charcoal, `#D9A441` Champagne Gold, `#FFF4DC` Cream, `#FFFFFF` White, `#F7F5F0` Neutral); elegant typography; subtle micro-animations (scale on hover, smooth ease).
- **NFR-4 (Architecture & Maintainability):** Monolithic Django SSR; DRY template inheritance (`base.html`, partials); context processors for global state.

### Additional Requirements & Architecture Invariants
- **AD-1:** Monolithic Django MVT with Server-Side Rendering (no SPA frameworks like React/Vue).
- **AD-2:** MySQL 8.0 with InnoDB engine and `utf8mb4_unicode_ci` charset.
- **AD-3:** Hybrid Session-First Cart with server-side price recalculation and authentication merge.
- **AD-4:** Standalone Tailwind CSS compilation pipeline.
- **AD-5:** Vanilla JavaScript ES6 micro-modules (slider, cart, mobile menu) without external dependencies.
- **Constraint:** Strictly no real payment gateway integration in MVP (mock checkout only).

---

## FR & NFR Coverage Map

| Requirement ID | Primary Epic / Story Coverage | Status |
| :--- | :--- | :---: |
| **FR-1.1 – FR-1.4** | Epic 1: Stories 1.3, 1.4; Epic 7: Story 7.2 | Covered |
| **FR-1.5** | Epic 5: Story 5.1 | Covered |
| **FR-1.6** | Epic 6: Story 6.3 | Covered |
| **FR-1.7** | Epic 1: Story 1.3 | Covered |
| **FR-2.1** | Epic 3: Story 3.1 | Covered |
| **FR-2.2** | Epic 2: Story 2.3; Epic 3: Story 3.2 | Covered |
| **FR-2.3** | Epic 1: Story 1.4 | Covered |
| **FR-2.4** | Epic 1: Story 1.4; Epic 8: Story 8.4 | Covered |
| **FR-3.1 – FR-3.2** | Epic 2: Story 2.1; Epic 4: Story 4.1 | Covered |
| **FR-3.3** | Epic 4: Story 4.2 | Covered |
| **FR-3.4** | Epic 2: Story 2.3; Epic 4: Story 4.1 | Covered |
| **FR-4.1 – FR-4.3** | Epic 5: Stories 5.1, 5.2 | Covered |
| **FR-5.1 – FR-5.3** | Epic 6: Stories 6.1, 6.2, 6.3 | Covered |
| **FR-5.4** | Epic 6: Story 6.4 | Covered |
| **FR-6.1** | Epic 8: Story 8.1 | Covered |
| **FR-6.2 – FR-6.3** | Epic 8: Stories 8.2, 8.3 | Covered |
| **FR-7.1 – FR-7.4** | Epic 7: Stories 7.1, 7.2, 7.3 | Covered |
| **FR-8.1 – FR-8.3** | Epic 1: Story 1.1; Epic 2: Stories 2.1, 2.2 | Covered |
| **NFR-1 – NFR-4** | Verified across all Epics & Stories | Covered |

---

## Epic List

1. **Epic 1: Project Foundation, Core Layout & Design System**
2. **Epic 2: Product Catalog & Database Infrastructure**
3. **Epic 3: Home Page Experience & Merchandising**
4. **Epic 4: Category Exploration & Interactive Lookbook Slider**
5. **Epic 5: Product Discovery & Search System**
6. **Epic 6: Customer Shopping Cart & Order Preparation**
7. **Epic 7: Customer Authentication & Profile Management**
8. **Epic 8: Brand Information, Contact Inquiries & Newsletter**

---

## Epic 1: Project Foundation, Core Layout & Design System
**Goal:** Initialize the Django codebase, configure MySQL database access, isolate environmental variables, establish the Tailwind CSS luxury design system, and build the reusable base layout template with header and footer.

### Story 1.1: Django Project Initialization, MySQL Database Configuration, and Environment Isolation
As a developer,  
I want to initialize the Django project structure, configure `.env` management, and establish a connection to MySQL 8.0,  
So that the development environment is secure, robust, and ready for domain application development.

**Acceptance Criteria:**
- **Given** a fresh workspace, **When** Django and required libraries (`mysqlclient`, `python-dotenv`, `pillow`) are installed, **Then** `manage.py` runs without errors.
- **Given** `.env` contains valid MySQL credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`), **When** `python manage.py check` is executed, **Then** a successful database connection to MySQL is established.
- **Given** `settings/` is organized into `base.py`, `development.py`, and `production.py`, **When** the application starts, **Then** `SECRET_KEY` and database credentials are read from environment variables and not hardcoded.
- **Given** the apps directory `apps/` is created, **When** domain apps (`core`, `catalog`, `cart`, `accounts`) are registered in `INSTALLED_APPS`, **Then** Django resolves all app paths correctly.

### Story 1.2: Tailwind CSS Pipeline & Luxury Design System Token Configuration
As a frontend developer,  
I want to configure the Tailwind CSS compiler with the MAX VIEW luxury palette and typography tokens,  
So that UI components consistently render with the specified brand styling without ad-hoc inline styles.

**Acceptance Criteria:**
- **Given** `tailwind.config.js` is created, **When** the custom color palette is inspected, **Then** tokens exist for `luxury-black` (`#171717`), `luxury-charcoal` (`#262626`), `luxury-gold` (`#D9A441`), `luxury-cream` (`#FFF4DC`), `luxury-white` (`#FFFFFF`), and `luxury-neutral` (`#F7F5F0`).
- **Given** `static/src/input.css` is processed by the Tailwind build pipeline, **When** `styles.css` is generated in `static/css/`, **Then** utility classes like `bg-luxury-black`, `text-luxury-gold`, and `bg-luxury-charcoal` are available.
- **Given** Google Fonts (Playfair Display and Plus Jakarta Sans) are imported in the base HTML, **When** font utility classes `font-serif` and `font-sans` are applied, **Then** fonts render correctly across all viewports.

### Story 1.3: Master Base Template, Responsive Navigation Bar, and Mobile Drawer
As a shopper,  
I want to navigate the website using a luxury, responsive navbar on desktop and mobile,  
So that I can easily discover sections of the store from any page.

**Acceptance Criteria:**
- **Given** any page using `base.html`, **When** the header renders, **Then** the MAX VIEW logo, links (*New Shop*, *Home*, *Categories*, *About*, *Contact*), search bar, auth link, and cart icon are displayed.
- **Given** a user is on mobile (< 768px), **When** they tap the hamburger button, **Then** the mobile navigation drawer transitions smoothly into view without page jumping.
- **Given** the mobile drawer is open, **When** the user taps the close button or an external backdrop, **Then** the drawer closes seamlessly.
- **Given** an unauthenticated visitor, **When** inspecting the navbar auth icon, **Then** it links to `/accounts/login/`; **And** when logged in, it indicates user identity and links to `/accounts/logout/`.

### Story 1.4: 4-Column Luxury Footer and Benefits Showcase Grid
As a shopper,  
I want to see store guarantees and essential footer links at the bottom of the page,  
So that I understand store policies, shipping benefits, and support options.

**Acceptance Criteria:**
- **Given** a visitor navigates to any page extending `base.html`, **When** they scroll to the bottom, **Then** the 4-column footer is visible containing Brand manifesto, Shop links, Support links, and Newsletter capture.
- **Given** the footer renders, **When** checking copyright information, **Then** `© 2026 MAX VIEW — All Rights Reserved.` is displayed.
- **Given** the benefits showcase partial `benefits_grid.html` is rendered, **When** viewing the grid, **Then** all 4 value props appear with icons:
  1. *Free Shipping* — "On orders above ₹999"
  2. *Easy Returns* — "15 days return policy"
  3. *Secure Payment* — "Safe and secure checkout"
  4. *24/7 Support* — "We're here to help you"
- **Given** viewports ranging from 375px mobile to 1440px desktop, **When** the footer and benefits grid render, **Then** layout scales from single-column to responsive 4-column without text clipping.

---

## Epic 2: Product Catalog & Database Infrastructure
**Goal:** Create the MySQL models for categories, products, secondary images, and lookbook slides, establish Django admin governance, seed the database with initial fixtures, and build the reusable product card component.

### Story 2.1: Catalog Models & MySQL Migrations
As a developer,  
I want to create Django ORM models for `Category`, `Product`, `ProductImage`, and `LookbookSlide` with proper indexes,  
So that catalog data is stored reliably in MySQL with referential integrity.

**Acceptance Criteria:**
- **Given** `apps/catalog/models.py`, **When** `Category` is defined, **Then** it includes `name`, `slug` (unique), `description`, `image`, `display_order`, `is_active`, and `created_at`.
- **Given** `Product` is defined, **When** checking fields and constraints, **Then** it includes `category` (`ForeignKey` with `on_delete=models.PROTECT`), `name`, `slug` (unique), `sku` (unique), `description`, `price` (`DecimalField`), `rating` (`DecimalField`), `stock_quantity`, `is_trending` (`BooleanField`), `image`, `is_active`, and timestamps.
- **Given** `ProductImage` is defined, **When** related to `Product`, **Then** it uses `on_delete=models.CASCADE` and includes `image`, `alt_text`, and `display_order`.
- **Given** `LookbookSlide` is defined, **When** migrated, **Then** it includes `title`, `subtitle`, `image`, `category` (`SET_NULL`), `link_url`, `display_order`, and `is_active`.
- **Given** `python manage.py makemigrations catalog` and `migrate` are run, **When** inspected in MySQL, **Then** all tables and composite indexes (`idx_cat_active`, `idx_trending_active`) exist.

### Story 2.2: Django Admin Integration & Initial Catalog Data Fixtures Seeding
As a store administrator,  
I want to manage products and categories via Django Admin and seed baseline sample data,  
So that the store immediately displays verified catalog inventory.

**Acceptance Criteria:**
- **Given** `apps/catalog/admin.py`, **When** accessing `/admin/`, **Then** `CategoryAdmin` and `ProductAdmin` provide list display, search fields (`name`, `sku`), category filters, and `ProductImageInline`.
- **Given** initial seed data fixtures or migrations are executed, **When** querying MySQL, **Then** 4 categories exist: *Men's Wear* (`mens-wear`), *Women's Wear* (`womens-wear`), *Kids' Wear* (`kids-wear`), and *Accessories* (`accessories`).
- **Given** initial products are seeded, **When** checking prices, **Then** Men's Wear is ₹499.00, Women's Wear is ₹599.00, Kids' Wear is ₹499.00, and Accessories is ₹899.00, all flagged `is_trending=True`.

### Story 2.3: Reusable Product Card Component with Gold Star Ratings & Hover Animations
As a shopper,  
I want to view product cards featuring elegant typography, champagne gold rating stars, and image zoom on hover,  
So that browsing items feels luxurious and interactive.

**Acceptance Criteria:**
- **Given** the partial `components/product_card.html`, **When** passed a product object, **Then** it renders image, category name, product title, description preview, formatted price (`₹<price>`), and gold star rating icons (`#D9A441`).
- **Given** a user hovers over the card image on desktop, **When** cursor enters, **Then** the image smoothly zooms (`scale-105 transition-transform duration-300`) without overflowing the card container.
- **Given** the product card renders, **When** clicking the product image or title, **Then** it routes to `catalog:product_detail` with the product slug.
- **Given** an "Add to Cart" button on the card, **When** clicked, **Then** it posts to the cart addition endpoint for that product ID.

---

## Epic 3: Home Page Experience & Merchandising
**Goal:** Deliver the luxury Home page experience featuring the editorial Hero section with dual photography and promotional offer badge, the Trending Arrivals product grid, and dynamic site settings.

### Story 3.1: Home Page Hero Section with Dual Imagery & Sale Badge
As a fashion shopper,  
I want to view a luxury hero section with brand messaging and sale highlights upon visiting the site,  
So that I am immediately impressed by the brand's style and motivated to shop.

**Acceptance Criteria:**
- **Given** a user visits `/`, **When** the hero section loads, **Then** the left column displays the brand heading, short description (*"Premium fashion bringing modern trends with uncompromising quality and style."*), and a "Shop Now" primary CTA button.
- **Given** the "Shop Now" button is clicked, **When** pressed, **Then** the user is navigated to the Categories catalog page (`/shop/categories/`).
- **Given** the hero's right column, **When** rendered, **Then** it displays a primary high-fashion visual, an overlapping supporting visual with subtle hover effect, and a sale-offer percentage badge (*"Exclusive Offer / Up to 40% Off"*).
- **Given** an "Explore Details" secondary link, **When** clicked, **Then** the page smoothly scrolls down to the Trending Arrivals section.

### Story 3.2: Trending Arrivals Showcase Grid Integration
As a shopper,  
I want to view the Trending Arrivals grid on the home page displaying four curated items,  
So that I can see the latest high-demand fashion pieces across all categories.

**Acceptance Criteria:**
- **Given** `HomeView` executes, **When** querying products, **Then** it filters for `is_trending=True` and `is_active=True`, fetching exactly 4 items with `select_related('category')`.
- **Given** the Home page renders, **When** viewing the Trending Arrivals section, **Then** 4 product cards are displayed in a responsive grid (1 column mobile, 2 columns tablet, 4 columns desktop).
- **Given** the 4 seeded products, **When** displayed, **Then** each represents a distinct category (Men's Wear ₹499, Women's Wear ₹599, Kids' Wear ₹499, Accessories ₹899) with gold star ratings.

### Story 3.3: Global Site Configuration Context Processor
As a developer,  
I want site-wide parameters (address, phone, email, site name) served via a context processor,  
So that contact and header information is easily configurable without altering templates.

**Acceptance Criteria:**
- **Given** `apps.core.models.SiteConfig`, **When** instantiated in database, **Then** it holds `site_name` ("MAX VIEW"), `support_email`, `support_phone`, and `store_address` ("123@ Tirupur, Tamil Nadu, INDIA").
- **Given** `site_settings` context processor is active in `TEMPLATES`, **When** any template renders `{{ site_config.support_email }}`, **Then** the database value is displayed.
- **Given** no `SiteConfig` record exists in the database, **When** the context processor runs, **Then** it gracefully falls back to default settings without crashing the view.

---

## Epic 4: Category Exploration & Interactive Lookbook Slider
**Goal:** Implement the dedicated Categories page with isolated filtering across the 4 categories and an interactive horizontal touch/mouse image slider.

### Story 4.1: Category Browsing View & Strict Category Isolation Filtering
As a shopper,  
I want to view items filtered strictly by category without mixing unrelated products,  
So that I can focus entirely on the style of clothing I am seeking.

**Acceptance Criteria:**
- **Given** a user navigates to `/shop/categories/`, **When** no specific category is selected, **Then** all 4 category tabs (*Men's Wear*, *Women's Wear*, *Kids' Wear*, *Accessories*) are displayed with the default active category's products.
- **Given** a user clicks on "Women's Wear" (slug: `womens-wear`), **When** the page updates, **Then** only products belonging to `womens-wear` appear in the product grid.
- **Given** the filtered product grid, **When** inspected, **Then** zero products from Men's Wear, Kids' Wear, or Accessories are present.
- **Given** a category with zero active products, **When** selected, **Then** an elegant empty message appears stating "No products currently available in this collection."

### Story 4.2: Horizontal Lookbook Image Slider with Prev/Next Controls & Touch Swipe
As a mobile and desktop shopper,  
I want an interactive horizontal lookbook slider with smooth controls and touch gestures,  
So that I can visually browse editorial fashion collections.

**Acceptance Criteria:**
- **Given** the Category page loads, **When** viewing the lookbook slider, **Then** curated fashion slides are rendered horizontally with previous (`<`) and next (`>`) directional controls.
- **Given** a user clicks the next control button, **When** activated, **Then** the slider smoothly advances to the next slide with CSS hardware-accelerated transitions.
- **Given** a user views the slider on a mobile touchscreen, **When** they swipe horizontally (left or right), **Then** touchstart and touchend events translate the carousel to the appropriate slide without vertical scroll lock.
- **Given** high-resolution slide images, **When** hovered on desktop, **Then** a subtle image zoom is applied without causing layout shift or horizontal scrollbars on the window.

---

## Epic 5: Product Discovery & Search System
**Goal:** Implement a responsive keyword search feature allowing customers to search products by title and description, complete with a clean results view and zero-match fallback.

### Story 5.1: Global Keyword Search Processing & Results View
As a shopper,  
I want to enter search keywords in the navbar and view matching products,  
So that I can quickly find items matching specific garments or styles.

**Acceptance Criteria:**
- **Given** a user enters a query (e.g. "Linen", "Suit", "Gold") into the search input and submits, **When** `SearchView` receives the GET parameter `q`, **Then** it executes a sanitized query filtering `Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), is_active=True)`.
- **Given** matching products exist, **When** `/search/?q=...` renders, **Then** the results page displays the search query, total match count, and a responsive grid of matching product cards.
- **Given** special characters or HTML in the search query, **When** processed by Django, **Then** input is escaped and sanitized, preventing XSS injection.

### Story 5.2: Empty Search State & Catalog Return Navigation
As a shopper whose search returned no items,  
I want to see a helpful empty state message with a direct link back to all products,  
So that I do not encounter a dead end and can continue shopping.

**Acceptance Criteria:**
- **Given** a user submits a search query that yields zero matches (e.g., "xyz123"), **When** the search results page renders, **Then** an elegant message displays: *"No products found matching 'xyz123'"*.
- **Given** the empty state is displayed, **When** viewing the page, **Then** a prominent primary button *"Explore All Categories"* is provided.
- **Given** the user clicks *"Explore All Categories"*, **When** clicked, **Then** they are routed to `/shop/categories/`.

---

## Epic 6: Customer Shopping Cart & Order Preparation
**Goal:** Implement the shopping cart lifecycle using Django sessions, allowing shoppers to add items, modify quantities, remove items, calculate server-verified totals in INR, and review an order summary (mock checkout).

### Story 6.1: Session-Based Shopping Cart Engine & Add-to-Cart Action
As a shopper,  
I want to add products to my cart while browsing without needing to create an account first,  
So that I can collect items I wish to purchase seamlessly.

**Acceptance Criteria:**
- **Given** an anonymous visitor clicks "Add to Cart" on a product card, **When** the POST request is processed by `CartAddView`, **Then** the item is added to `request.session['cart']` with quantity = 1 (or incremented if already present).
- **Given** the item is added, **When** the response returns, **Then** a flash message confirms the product addition and the navbar cart counter increments immediately.
- **Given** an item out of stock (`stock_quantity=0`), **When** attempting to add to cart, **Then** the server rejects the addition and returns an informative notice.

### Story 6.2: Cart Detail View, Quantity Stepper, and Server-Side Subtotal Recalculation
As a customer,  
I want to view my cart and adjust item quantities with instant subtotal and total updates,  
So that I can review and adjust my order before proceeding.

**Acceptance Criteria:**
- **Given** a user visits `/cart/`, **When** the page renders, **Then** every item in the cart is listed with image, name, unit price, quantity stepper (`-` / `+`), and line item subtotal.
- **Given** a customer increments or decrements quantity, **When** the update is submitted, **Then** `CartUpdateView` validates available stock, recalculates line subtotal and order grand total on the server, and persists changes.
- **Given** cart calculations execute, **When** computing the grand total, **Then** prices are strictly fetched from the database `Product.price` rather than trusting client-submitted values.
- **Given** order subtotal is >= ₹999.00, **When** viewing shipping cost, **Then** Free Shipping is applied; otherwise, standard shipping is noted.

### Story 6.3: Cart Item Removal & Dynamic Navbar Badge Updates
As a customer,  
I want to remove items from my cart and have the cart indicator reflect the changes,  
So that I can eliminate items I no longer wish to buy.

**Acceptance Criteria:**
- **Given** an item in `/cart/`, **When** the customer clicks the remove / delete icon, **Then** `CartRemoveView` deletes the product entry from the session cart.
- **Given** an item is removed, **When** the view updates, **Then** the grand total recalculates and a success notification confirms the removal.
- **Given** all items are removed from the cart, **When** viewing `/cart/`, **Then** an empty cart message displays *"Your shopping bag is empty"* with a *"Continue Shopping"* button.
- **Given** any page load, **When** `cart_summary` context processor executes, **Then** the navbar cart icon displays the exact sum of all item quantities.

### Story 6.4: Mock Checkout Preview & Order Summary View
As a shopper ready to checkout,  
I want to view an order review screen summarizing my items, shipping address, and total,  
So that I can verify my order without undergoing real financial transactions.

**Acceptance Criteria:**
- **Given** a cart with at least one item, **When** the customer clicks "Proceed to Checkout", **Then** they are routed to `/cart/checkout/`.
- **Given** `/cart/checkout/` renders, **When** inspecting the layout, **Then** it presents an order summary (items, quantities, subtotal, shipping, grand total in ₹) and customer shipping address fields.
- **Given** the customer clicks "Place Order (Mock)", **When** submitted, **Then** a confirmation message displays *"Order placed successfully in demonstration mode"* and the active cart is cleared.
- **Given** an empty cart, **When** trying to access `/cart/checkout/`, **Then** the user is redirected to `/cart/` with an alert.

---

## Epic 7: Customer Authentication & Profile Management
**Goal:** Build secure customer registration, login, logout, and profile management using Django Authentication, including cart session synchronization upon login.

### Story 7.1: User Registration with Validation & Password Policy
As a new customer,  
I want to create an account with my name, email, username, and secure password,  
So that I can save my profile and enjoy an expedited shopping experience.

**Acceptance Criteria:**
- **Given** a user navigates to `/accounts/register/`, **When** viewing the form, **Then** fields for Full Name, Email, Username, Password, and Confirm Password are displayed.
- **Given** a user submits mismatched passwords or an existing username/email, **When** `RegistrationForm` validates, **Then** the form displays clear inline error messages and retains valid input.
- **Given** valid registration details are submitted, **When** processed by `UserRegistrationView`, **Then** a new `auth_user` record is created with a PBKDF2 hashed password, a `CustomerProfile` is created, and the user is redirected to `/accounts/login/` with a success notice.

### Story 7.2: Customer Login, Logout & Navbar Authentication State Toggle
As a registered customer,  
I want to log into my account and log out when finished,  
So that my account remains secure and my session state is recognized.

**Acceptance Criteria:**
- **Given** a registered user submits correct credentials at `/accounts/login/`, **When** authenticated by Django, **Then** a session is established and the user is redirected to the home page or previous page.
- **Given** an authenticated session, **When** inspecting the navbar, **Then** the user's name is displayed alongside a "Logout" action instead of "Login".
- **Given** the user clicks "Logout", **When** processed by `UserLogoutView`, **Then** the session is terminated and the navbar reverts to displaying the "Login" action.

### Story 7.3: Cart Synchronization upon Customer Authentication
As a customer who added items to my cart as a guest before logging in,  
I want my guest cart items merged with my account upon logging in,  
So that I do not lose selected items when authenticating.

**Acceptance Criteria:**
- **Given** a guest user has items in `request.session['cart']`, **When** they log into their account, **Then** `merge_session_cart_to_db` transfers all session items into their database `Cart` record.
- **Given** an item in the session cart already exists in the database cart, **When** merged, **Then** quantities are summed (capped at inventory limits).
- **Given** the merge completes, **When** visiting `/cart/`, **Then** the cart contains the unified item list.

---

## Epic 8: Brand Information, Contact Inquiries & Newsletter
**Goal:** Deliver the About Us page, Contact Us page with store details and validated inquiry form, configurable Careers link, and footer newsletter subscription capture.

### Story 8.1: About Us Page Layout & Brand Heritage Presentation
As a brand-conscious shopper,  
I want to learn about the history and mission of MAX VIEW,  
So that I feel connected to the craftsmanship and identity of the brand.

**Acceptance Criteria:**
- **Given** a user visits `/about/`, **When** the page renders, **Then** the heading "ABOUT US", brand story blurb, and mission statement are displayed using editorial typography and balanced spacing.
- **Given** the visual layout, **When** inspected, **Then** high-fashion imagery and subtle hover effects are present, matching the luxury palette.
- **Given** responsive breakpoints, **When** viewing on mobile, tablet, and desktop, **Then** text hierarchy and image containers remain properly aligned without horizontal scrollbars.

### Story 8.2: Contact Us Page with Business Information & Configurable Careers Anchor
As a customer or job seeker,  
I want to view store contact coordinates and explore career opportunities,  
So that I know where the store is located and how to connect with the brand.

**Acceptance Criteria:**
- **Given** a user visits `/contact/`, **When** the page renders, **Then** store address (*123@ Tirupur, Tamil Nadu, INDIA*), telephone (*1234567890*), and email (*maxview1@gmail.com*) are clearly displayed alongside a store photo.
- **Given** the Careers section, **When** viewed, **Then** heading *"Careers at MAX VIEW"*, accompanying description (*"Learn more about our teams and job openings."*), and *"Explore Jobs"* button are rendered.
- **Given** the *"Explore Jobs"* button, **When** clicked, **Then** it routes to the configured careers destination without creating broken links.

### Story 8.3: Contact Ingestion Form with CSRF Protection & MySQL Storage
As a customer with questions,  
I want to submit an inquiry through the Contact form,  
So that customer service can assist me with my order or inquiry.

**Acceptance Criteria:**
- **Given** the contact form on `/contact/`, **When** viewed, **Then** fields for Name, Email, Subject, and Message are displayed with a "Send Message" button and CSRF token.
- **Given** a user submits invalid data (e.g. malformed email or empty required fields), **When** server validation runs, **Then** errors are highlighted on the form.
- **Given** valid data is submitted, **When** processed by `ContactView`, **Then** a new record is saved in MySQL (`core_contactmessage`) with `is_resolved=False` and a success banner confirms receipt.

### Story 8.4: Newsletter Subscription Ingestion & Client/Server Validation
As a fashion enthusiast,  
I want to subscribe to the newsletter from the footer,  
So that I receive announcements about exclusive collections and promotions.

**Acceptance Criteria:**
- **Given** the newsletter capture form in the footer, **When** a user enters a valid email address and clicks "Subscribe", **Then** the request is sent via AJAX/POST to `NewsletterSubscribeView`.
- **Given** an already registered email, **When** submitted, **Then** the response gracefully confirms the user is already subscribed without exposing database errors.
- **Given** a new valid email, **When** saved, **Then** a record is created in `core_newslettersubscriber` in MySQL and a toast notification confirms subscription.

---

## Technical Implementation Order Summary

```
Phase 1: Foundation & Setup
  └── Story 1.1: Django + MySQL + Environment Setup
  └── Story 1.2: Tailwind CSS Luxury Pipeline Setup
  └── Story 1.3: Master Base Template & Responsive Navbar
  └── Story 1.4: 4-Column Luxury Footer & Benefits Grid

Phase 2: Data Models & Catalog Infrastructure
  └── Story 2.1: Catalog Models & MySQL Migrations
  └── Story 2.2: Django Admin & Initial Data Seed Fixtures
  └── Story 2.3: Reusable Product Card Component

Phase 3: Merchandising & Discovery Views
  └── Story 3.1: Home Page Hero & Sale Offer Badge
  └── Story 3.2: Trending Arrivals Grid Integration
  └── Story 3.3: Site Configuration Context Processor
  └── Story 4.1: Category View & Strict Filtering
  └── Story 4.2: Horizontal Lookbook Image Slider
  └── Story 5.1: Keyword Search Engine & Results Page
  └── Story 5.2: Empty Search State & Recovery Navigation

Phase 4: Commerce Engine (Cart & Mock Checkout)
  └── Story 6.1: Session Cart Engine & Add-to-Cart
  └── Story 6.2: Cart Detail, Stepper & Subtotal Recalculation
  └── Story 6.3: Cart Removal & Navbar Badge Updates
  └── Story 6.4: Mock Checkout Preview & Review

Phase 5: Authentication & Session Continuity
  └── Story 7.1: User Registration & Password Hashing
  └── Story 7.2: User Login, Logout & Navbar State
  └── Story 7.3: Cart Synchronization on Authentication

Phase 6: Information Pages & Engagement
  └── Story 8.1: About Us Page Layout & Brand Story
  └── Story 8.2: Contact Us & Careers Anchor
  └── Story 8.3: Contact Ingestion Form & MySQL Storage
  └── Story 8.4: Newsletter Subscription Ingestion
```

---

## Review and Acceptance Sign-off

- **Spec Author:** BMad Strategy & Architecture Team
- **File Path:** `_bmad-output/user-stories/epics.md`
- **Application Code Status:** 0% authored (Strictly adhering to requirement: No implementation code written yet)
- **Status:** Complete and ready for stakeholder review.
