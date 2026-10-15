# Product Requirements Document (PRD)
## MAX VIEW — Luxury Fashion E-Commerce Platform

---

### Document Metadata
- **Project Name:** MAX VIEW Luxury Fashion E-Commerce
- **Document Version:** 1.0.0
- **Document Status:** Draft for Review
- **Author:** John, Product Manager (BMad Method)
- **Stakeholder:** GT
- **Date:** October 14, 2026
- **Location:** `_bmad-output/prds/PRD.md`

---

## 1. Executive Summary & Product Vision

### 1.1 Vision Statement
**MAX VIEW** is an exclusive, modern luxury fashion e-commerce platform designed to offer discerning customers a curated, high-end shopping experience. The platform combines a refined minimalist aesthetic (champagne gold, deep charcoal, rich black, and soft cream) with effortless performance, clear navigation, and robust catalog discovery.

### 1.2 Core Objective
To engineer and deliver a production-ready, highly responsive fashion e-commerce web application utilizing **Python Django**, **Django HTML Templates**, **Tailwind CSS**, **Vanilla JavaScript**, and **MySQL**. The system balances editorial visual sophistication with dependable e-commerce mechanics, including categorized browsing, interactive image sliders, real-time product search, session/database cart management, and secure customer authentication.

### 1.3 Key Value Proposition
- **High-End Aesthetics:** Tailored fashion-house feel avoiding generic styling; subtle hover micro-interactions, editorial typography, and disciplined color harmony.
- **Frictionless Shopping Flow:** Instant category switching, touch-friendly image carousels, and persistent shopping cart without external framework bloat.
- **Architectural Simplicity & Reliability:** Server-rendered Django architecture with server-side validation and MySQL persistence, avoiding unnecessary client-side framework complexity.

---

## 2. Target Audience & User Roles

| Role | Description | Core Goals & Capabilities |
| :--- | :--- | :--- |
| **Guest / Visitor** | Unauthenticated shopper browsing on desktop, tablet, or mobile. | Explore home and category pages, search catalog, inspect product details, add/edit cart items, submit contact queries, subscribe to newsletter, create account. |
| **Registered Customer** | Authenticated shopper with persistent profile state. | Secure login/logout, manage active cart across sessions, expedited mock checkout flow, profile continuity. |
| **Store Administrator** | Business owner or inventory manager via Django Admin. | Manage categories, products, images, stock levels, view customer inquiries, export newsletter subscriber lists. |

---

## 3. Product Scope & Delivery Boundaries

### 3.1 In-Scope (MVP Release)
1. **Core Navigation & Layout:** Responsive, sticky/accessible navbar with authentication toggles and cart counter; luxury 4-column footer with newsletter capture.
2. **Page 1 — Home Experience:**
   - Editorial Hero Section with brand statement, CTA ("Shop Now"), dual fashion visuals, and sale-offer badge.
   - Trending Arrivals grid (Men's, Women's, Kids', Accessories) with prices (₹), ratings, and quick actions.
   - 4-Pillar Value Proposition Grid (Free Shipping, Easy Returns, Secure Payment, 24/7 Support).
3. **Page 2 — Categories & Discovery:**
   - 4 Dedicated Categories: Men's Wear, Women's Wear, Kids' Wear, Accessories.
   - Dynamic, isolated category filtering (no cross-category contamination).
   - Interactive horizontal touch/mouse image slider with prev/next controls and zoom.
   - Uniform product cards with INR pricing, gold star ratings, and detail modals/views.
4. **Page 3 — About Us:**
   - Brand heritage narrative, mission statement, editorial imagery, and responsive typography.
5. **Page 4 — Contact Us & Careers Hook:**
   - Store physical and digital contact details (Tirupur hub, phone, email).
   - CSRF-protected contact message submission form with server-side feedback.
   - Configurable "Careers at Forever / MAX VIEW" exploratory link.
6. **Page 5 — Authentication (Login & Register):**
   - User registration (Name, Email, Username, Password verification).
   - Secure Django authentication login with error feedback and redirection.
   - Dynamic navbar state reflecting logged-in user status.
7. **Cross-Cutting Capabilities:**
   - Keyword search across product titles and descriptions with zero-match fallbacks.
   - Complete cart lifecycle (Add, Update Quantity, Remove, Subtotal & Grand Total calculation).
   - MySQL database integration with Django ORM models and migrations.

### 3.2 Explicitly Out of Scope (Post-MVP Roadmap)
- Real payment gateway integration (Stripe, Razorpay, etc.) — payment will be mocked or deferred per explicit instruction.
- Third-party courier/logistics tracking APIs.
- Full-scale multi-tier job recruitment portal (careers link is configurable external or placeholder).
- User-generated product reviews and photo uploads (ratings will be admin/catalog driven in MVP).
- Single Page Application (SPA) frameworks (no React, Vue, or Angular).

---

## 4. Key Assumptions & Constraints

### 4.1 Confirmed Constraints
- **Tech Stack Mandate:** Python Django, Django HTML Templates, Tailwind CSS, JavaScript, and MySQL. No React or modern frontend SPA frameworks.
- **Visual Identity:** Luxury palette adhering strictly to:
  - Premium Black: `#171717`
  - Deep Charcoal: `#262626`
  - Champagne Gold: `#D9A441`
  - Cream: `#FFF4DC`
  - White: `#FFFFFF`
  - Soft Neutral: `#F7F5F0`
- **Commercial Boundary:** No real payment gateway will be deployed without explicit prior stakeholder sign-off.

### 4.2 Documented Assumptions & Discrepancies
1. **Brand Identity Consistency (`[ASSUMPTION]`):** Section 3 of the source requirements refers to the brand story as *"Max Collection"*, while the document title and navbar specify *"MAX VIEW"*. 
   - *Working Assumption:* **MAX VIEW** is the primary parent brand name; "Max Collection" will be harmonized as MAX VIEW's signature collection unless directed otherwise by the stakeholder.
2. **Careers Section Title (`[ASSUMPTION]`):** Section 4 references *"Careers at Forever"*.
   - *Working Assumption:* This is a legacy or boilerplate reference. The copy will default to *"Careers at MAX VIEW"* with configurable route/URL options.
3. **Contact Details Placeholders (`[ASSUMPTION]`):** The address (*123@ Tirupur, Tamil Nadu*), telephone (*1234567890*), and email (*maxview1@gmail.com*) are sample demonstration records. They must be stored in Django settings or a site-configuration model so they can be changed without modifying templates.
4. **Initial Product Pricing (`[ASSUMPTION]`):** Stated prices (₹499 Men's, ₹599 Women's, ₹499 Kids', ₹899 Accessories) are seeded sample data loaded into MySQL via Django fixtures or data migrations.

---

## 5. Functional Requirements (FR)

### FR-1: Global Navigation & Header System
- **FR-1.1:** The navbar must be present and identical across all views via a shared `base.html` and `navbar.html` partial.
- **FR-1.2:** Brand identity: Display the MAX VIEW logo linking directly to the Home route (`/`).
- **FR-1.3:** Navigation links must map cleanly to distinct routes: *New Shop*, *Home*, *Categories*, *About*, *Contact*.
- **FR-1.4:** Auth state reflection:
  - If anonymous: Display *Login* / *Register* action icons/links.
  - If authenticated: Display user indicator and *Logout* action.
- **FR-1.5:** Global Search Bar: Include an accessible input and search icon that triggers keyword search upon submission.
- **FR-1.6:** Cart Indicator: Display a shopping cart icon with a dynamic badge indicating the total count of active items; clicking opens the cart page (`/cart/`).
- **FR-1.7:** Mobile Navigation: Implement a touch-friendly hamburger toggle that collapses navigation items seamlessly on viewports `< 768px`.

### FR-2: Home Page Presentation & Merchandising
- **FR-2.1 Hero Section:**
  - Display brand headline and description: *"Premium fashion bringing modern trends with uncompromising quality and style."*
  - Prominent "Shop Now" primary CTA button routing to the catalog/category view.
  - High-resolution editorial fashion image pair with subtle hover zoom effect.
  - Prominent sale-offer percentage badge (e.g., *"Exclusive Offer / Up to 40% Off"*).
  - Secondary "Explore Details" link scrolling to featured items or opening brand story.
- **FR-2.2 Trending Arrivals Grid:**
  - Display four curated product cards in a responsive grid (1 col mobile, 2 col tablet, 4 col desktop).
  - Each card must display:
    1. Uniformly sized high-fashion product image.
    2. Category tag & Product Title.
    3. Truncated product summary/description.
    4. 5-star visual rating using champagne-gold star icons.
    5. Price formatted in Indian Rupees (e.g., `₹499`).
    6. "View Details" or "Add to Cart" interaction.
  - Hover micro-animation: Subtle image scale (`scale-105`) and elevation shadow.
- **FR-2.3 Benefits Showcase Grid:**
  - 4-item responsive card grid featuring icon, bold headline, and subtitle:
    1. *Free Shipping* — "On orders above ₹999"
    2. *Easy Returns* — "15 days return policy"
    3. *Secure Payment* — "Safe and secure checkout"
    4. *24/7 Support* — "We're here to help you"
- **FR-2.4 Global Luxury Footer:**
  - Section 1 (Brand): MAX VIEW brand manifesto and copyright `© 2026 MAX VIEW — All Rights Reserved.`
  - Section 2 (Shop): Links to *New Arrivals*, *Best Sellers*, *Exclusive Offers*, *Gift Cards*.
  - Section 3 (Support): Links to *Shipping Info*, *Returns & Exchanges*, *Size Guide*, *Contact Us*.
  - Section 4 (Newsletter): Email capture form with client-side & server-side email validation and instant confirmation messaging upon subscription.

### FR-3: Category Hierarchy & Interactive Showcase
- **FR-3.1 Category Taxonomy:** Support four distinct categories:
  - `mens-wear` (Men's Wear)
  - `womens-wear` (Women's Wear)
  - `kids-wear` (Kids' Wear)
  - `accessories` (Accessories)
- **FR-3.2 Category Filtering:** Clicking a category tab or pill dynamically filters the product grid to show strictly products belonging to that category. No products from outside the active category may bleed through.
- **FR-3.3 Horizontal Image Slider:**
  - Prominent horizontal slider showcasing curated fashion looks sliding left-to-right.
  - Must feature visible previous (`<`) and next (`>`) directional controls.
  - Must support touch swiping on mobile devices without layout overflow.
  - Smooth hardware-accelerated CSS/JS transitions and subtle image zoom on hover.
- **FR-3.4 Product Card Grid:** Render active category products with photo, name, description, rating, price, and add-to-cart action.

### FR-4: Product Search Experience
- **FR-4.1 Query Processing:** Process user-submitted search queries across product `name`, `description`, and `category__name`.
- **FR-4.2 Result Presentation:** Render matching product cards in the standard product grid layout with count of matching items.
- **FR-4.3 Zero-Match Fallback:** When a query yields no records, display an elegant "No products found matching your search" message along with a "Clear Search / View All Products" button.

### FR-5: Shopping Cart & Order Preparation
- **FR-5.1 Cart Storage:** Maintain cart state via Django session backend for guest visitors, with synchronization on user login.
- **FR-5.2 Cart Operations:**
  - *Add to Cart:* Add product with specified quantity; increment if already present.
  - *Update Quantity:* Change item count with real-time recalculation of item subtotal.
  - *Remove Item:* Instantly delete line item from cart.
- **FR-5.3 Price & Calculation Integrity:** All subtotal and grand total calculations must be strictly computed on the server side using canonical database price values. Never trust client-submitted prices.
- **FR-5.4 Mock Checkout State:** Provide a "Proceed to Checkout" action that validates cart items and presents an order review screen without invoking real external charge APIs.

### FR-6: Brand Heritage & Contact Systems
- **FR-6.1 About Us Page:**
  - Showcase editorial brand imagery paired with the official Brand Story and Mission text.
  - Maintain typography hierarchy, balanced negative space, and cohesive luxury palette.
- **FR-6.2 Contact Us Page:**
  - Display verified business details: Address (*Tirupur, Tamil Nadu*), Telephone (*1234567890*), Email (*maxview1@gmail.com*).
  - Careers Section: Display *"Careers at MAX VIEW"*, accompanying blurb, and "Explore Jobs" button routing to configurable contact/careers anchor.
- **FR-6.3 Contact Ingestion Form:**
  - Form fields: Name (text), Email (email), Subject (text), Message (textarea).
  - Validation: Django Form / ModelForm validation with CSRF token verification.
  - Persistence: Store contact inquiries in the MySQL database via `ContactMessage` model and render a success message toast/banner upon submission.

### FR-7: Customer Authentication & Access Control
- **FR-7.1 Registration:** Collect full name, email, username, password, and password confirmation. Ensure unique username/email constraints and Django standard password validators.
- **FR-7.2 Authentication:** Standard Django session authentication supporting login via username/email and password.
- **FR-7.3 Logout:** Secure session termination with redirection to home or login page with confirmation message.
- **FR-7.4 Security:** Implement protection against brute force, CSRF injection, and ensure password hashes are salted and hashed (PBKDF2/argon2).

### FR-8: Database & Administration Model
- **FR-8.1 Data Persistence:** All application entities must reside in MySQL relational tables managed via Django migrations.
- **FR-8.2 Core Entities:**
  - `Category`: `id`, `name`, `slug`, `description`, `image`, `created_at`
  - `Product`: `id`, `category` (FK), `name`, `slug`, `description`, `price`, `rating`, `stock`, `is_trending`, `image`, `created_at`
  - `Cart` & `CartItem`: Session key / User (FK), Product (FK), Quantity, Created/Updated
  - `ContactMessage`: Name, Email, Subject, Message, Created timestamp, Is resolved
  - `NewsletterSubscriber`: Email, Subscribed timestamp, Is active
- **FR-8.3 Django Admin:** Provide administrative interface for catalog seeding, image uploading, and inquiry monitoring.

---

## 6. Non-Functional Requirements (NFR)

### 6.1 Performance & Responsiveness
- **NFR-1.1 Page Load Speed:** First Contentful Paint (FCP) under 1.5 seconds on desktop and under 2.5 seconds on 4G mobile.
- **NFR-1.2 Image Optimization:** Static and media fashion images must be sized, compressed, and lazy-loaded to prevent layout shifts (CLS < 0.1).
- **NFR-1.3 Zero Layout Overflow:** Mobile and tablet viewports (320px to 1024px) must not exhibit horizontal window scrollbars or clipped interactive targets.

### 6.2 Security & Data Protection
- **NFR-2.1 CSRF Protection:** 100% of state-altering HTTP POST requests (forms, cart updates, newsletter submissions) must include valid Django CSRF tokens.
- **NFR-2.2 SQL Injection & XSS Prevention:** Rely strictly on Django ORM parameterized queries and template auto-escaping. Never use raw SQL string interpolation.
- **NFR-2.3 Credential Isolation:** Database passwords, secret keys, and configuration parameters must be loaded via environment variables (`.env`) and never committed into source control.

### 6.3 UI/UX Design System Compliance
- **NFR-3.1 Color Fidelity:** Strict implementation of specified hexadecimal values:
  - `#171717` (Premium Black - Backgrounds, primary text)
  - `#262626` (Deep Charcoal - Cards, secondary backgrounds)
  - `#D9A441` (Champagne Gold - Accents, rating stars, active badges, primary CTA highlights)
  - `#FFF4DC` (Cream - Soft contrast text, pill tags)
  - `#FFFFFF` (White - Pure highlights, contrast elements)
  - `#F7F5F0` (Soft Neutral - Clean contrast sections)
- **NFR-3.2 Typography & Spacing:** Editorial serif or refined sans-serif headings with generous leading and proportional margins.
- **NFR-3.3 Micro-Animations:** Subtle transitions (150ms-300ms ease) on buttons, links, card hover states, and image slider movements.

### 6.4 Maintainability & Extensibility
- **NFR-4.1 Template Architecture:** DRY (Don't Repeat Yourself) architecture with `base.html`, reusable partials (`navbar.html`, `footer.html`, `product_card.html`), and template inheritance.
- **NFR-4.2 Code Cleanliness:** Clean separation of concerns between Django views, models, forms, static JavaScript modules, and Tailwind CSS styles.

---

## 7. User Stories & Acceptance Criteria

### Epic 1: Catalog Exploration & Product Discovery

#### Story 1.1: Home Page & Trending Arrivals
> **As a** fashion shopper,  
> **I want to** view a luxury home page featuring brand highlights and trending arrivals,  
> **So that** I can immediately understand the brand aesthetic and discover featured products.

- **AC 1.1.1:** Given a visitor navigates to `/`, when the page loads, then the luxury hero section displays the brand description, "Shop Now" button, and sale-offer badge.
- **AC 1.1.2:** Given the visitor scrolls down, when viewing the Trending Arrivals section, then four distinct product cards (Men's, Women's, Kids', Accessories) are displayed with images, titles, descriptions, gold star ratings, and prices in ₹.
- **AC 1.1.3:** Given a user hovers over any product card, when the mouse enters the image area, then the image smoothly zooms without overflowing the card boundaries.
- **AC 1.1.4:** Given the user reaches the bottom of the page, then the 4-column footer and benefits grid are fully visible.

#### Story 1.2: Category Filtering & Slider Experience
> **As a** shopper interested in specific attire,  
> **I want to** switch between fashion categories and browse lookbooks via an interactive slider,  
> **So that** I can explore items relevant to my personal style without clutter.

- **AC 1.2.1:** Given a user is on the Categories page, when they click on "Men's Wear", then only Men's Wear products appear in the grid, and products from other categories are hidden.
- **AC 1.2.2:** Given a user views the image slider, when clicking the next/previous navigation controls, then the slider advances smoothly left-to-right to the next lookbook image.
- **AC 1.2.3:** Given a mobile user touches the slider, when swiping horizontally, then the slider translates smoothly to the next image without triggering vertical page scrolling lock.

#### Story 1.3: Real-Time Product Search
> **As a** shopper looking for specific items,  
> **I want to** enter search terms into the navbar search bar,  
> **So that** I can quickly locate matching fashion products.

- **AC 1.3.1:** Given a user enters a search keyword (e.g., "Silk", "Jacket") into the search box and presses enter, when the query executes, then the results page displays all matching products.
- **AC 1.3.2:** Given no products match the query, when the search results page renders, then a clean zero-state message appears with a button to return to the catalog.

---

### Epic 2: Shopping Cart & Purchase Flow

#### Story 2.1: Cart Item Management
> **As a** customer,  
> **I want to** add products to my cart, adjust item quantities, and remove unwanted items,  
> **So that** I can organize my intended purchases before checking out.

- **AC 2.1.1:** Given a user clicks "Add to Cart" on a product card, when the request completes, then the navbar cart counter increments and a confirmation message is displayed.
- **AC 2.1.2:** Given a user navigates to `/cart/`, when modifying an item's quantity input, then the line item total and the order grand total recalculate accurately on the server.
- **AC 2.1.3:** Given a user clicks the remove icon on a cart item, when confirmed, then the item is removed from the cart and totals update immediately.
- **AC 2.1.4:** Given guest users add items to the cart, when they close and reopen their browser session, then their cart items remain intact via session storage.

---

### Epic 3: Customer Authentication & Profile Security

#### Story 3.1: Account Registration & Login
> **As a** returning shopper,  
> **I want to** register an account and log in securely,  
> **So that** my preferences and cart remain attached to my identity.

- **AC 3.1.1:** Given a new user visits `/register/`, when they submit valid registration details (name, email, unique username, matching passwords), then a new Django user is created and they are redirected to login.
- **AC 3.1.2:** Given a registered user visits `/login/`, when they provide correct credentials, then they are authenticated and redirected, and the navbar updates to show "Logout".
- **AC 3.1.3:** Given invalid credentials are submitted, when the form re-renders, then clear, non-leaking error feedback is displayed without crashing the view.

---

### Epic 4: Information, Contact & Engagement

#### Story 4.1: Contact Inquiry & Newsletter Sign-up
> **As a** website visitor,  
> **I want to** send inquiries to customer service and subscribe to newsletter updates,  
> **So that** I can receive assistance and stay informed on exclusive offers.

- **AC 4.1.1:** Given a user fills out the Contact form with name, valid email, subject, and message, when they click "Send Message", then the record is saved to MySQL and a success feedback alert appears.
- **AC 4.1.2:** Given an invalid email is entered into the footer newsletter input, when submitted, then client-side and server-side validation reject the submission with an appropriate error notice.

---

## 8. Verification & Acceptance Checklist

| # | Acceptance Criterion | Verification Method | Status |
| :---: | :--- | :--- | :---: |
| 1 | All 5 primary page views load with correct routes and templates | Manual & URL route testing | Pending Review |
| 2 | Consistent navbar and footer rendered across 100% of pages | Template partial inspection | Pending Review |
| 3 | All navigation links resolve to valid, working endpoints (no broken 404s) | Route crawl validation | Pending Review |
| 4 | Home page exhibits Hero, 4-product grid, benefits grid, and footer | Visual & DOM inspection | Pending Review |
| 5 | Category filtering displays only products belonging to the chosen category | Filter interaction testing | Pending Review |
| 6 | Image slider features functional prev/next controls and touch swipe | Browser emulation testing | Pending Review |
| 7 | Search bar accurately filters products and gracefully handles zero matches | Keyword query tests | Pending Review |
| 8 | Django authentication operates correctly for register, login, and logout | Form submission & auth tests | Pending Review |
| 9 | Cart supports add, quantity change, item removal, and accurate totals | Cart lifecycle tests | Pending Review |
| 10 | Contact and newsletter forms validate inputs and persist to database | Form submission & DB check | Pending Review |
| 11 | Static/media images load reliably without 404 or broken placeholders | Network asset inspection | Pending Review |
| 12 | MySQL relational database stores models, products, and submissions | Database query inspection | Pending Review |
| 13 | Responsive design functions smoothly across mobile (375px), tablet, desktop | Responsive viewport tests | Pending Review |
| 14 | No unnecessary existing project functionality is degraded or removed | Regression inspection | Pending Review |
| 15 | No real payment gateway processing is introduced without authorization | Architectural audit | Verified In Scope |

---

## 9. Next Steps & Approval Gate

1. **Stakeholder Review:** Review of this PRD by GT.
2. **Approval Sign-off:** Confirmation to proceed from PRD phase into **Technical Architecture** (`_bmad-output/architecture/`) and **Database Design** (`_bmad-output/database/`).
3. **No Application Code Execution:** In strict adherence to your instructions, no Django code or migrations have been authored yet.
