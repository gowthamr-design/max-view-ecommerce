# BMAD PRD — MAX VIEW Luxury Fashion E-commerce Website

## Project Objective

Build a simple, modern, luxury fashion e-commerce website named **MAX VIEW** using Django, HTML Templates, Tailwind CSS, JavaScript, and MySQL.

The website must have a premium fashion-store appearance, high-quality images, elegant typography, responsive layouts, subtle hover animations, and fully functional navigation.

## Technology Stack

- Backend: Python Django
- Frontend: Django HTML Templates
- Styling: Tailwind CSS
- Interactions: JavaScript
- Database: MySQL
- Authentication: Django Authentication
- Images: Django static and media files

## Important Instructions

1. Follow the requirements in this document.
2. Do not mention or reference any external or existing website.
3. Separate confirmed requirements from assumptions.
4. Build reusable Django templates, a shared navbar, and a shared footer.
5. Use a premium black, cream, white, and champagne-gold color palette.
6. Use suitable high-quality fashion images.
7. Ensure all navigation, forms, category selection, search, and cart interactions work correctly.
8. Do not introduce React or another frontend framework.
9. Do not implement real payment processing unless explicitly requested.
10. Inspect the project files before modifying existing code. Avoid unnecessary changes to working functionality.

# PAGE 1 — HOME

## Navbar

Create a responsive navbar containing:

- MAX VIEW logo.
- New Shop.
- Home.
- Categories.
- About.
- Contact.
- Logout.
- Search box and search icon.
- User/Login icon.
- My Cart icon.

Requirements:

- Connect every navigation item to the appropriate Django URL.
- Display Login or Logout based on authentication status.
- Make search functional.
- Make the cart icon navigate to the cart page.
- Add subtle hover effects and a mobile hamburger menu.

## Hero Section

Create a luxury fashion hero section.

Layout:

- Left side: Brand heading, short description, and Shop Now button.
- Right side: Large fashion image and a supporting image with hover effects.
- Include a sale-offer percentage badge.
- Include an Explore Details link.

Brand description:
"Premium fashion bringing modern trends with uncompromising quality and style."

Use elegant spacing, premium photography, and responsive layouts.

## Trending Arrivals

Display four product cards in a responsive grid.

### Product 1 — Men's Wear

- Premium fashion image.
- Product name and description.
- Star rating.
- Price: ₹499.

### Product 2 — Women's Wear

- Premium fashion image.
- Product name and description.
- Star rating.
- Price: ₹599.

### Product 3 — Kids' Wear

- Premium fashion image.
- Product name and description.
- Star rating.
- Price: ₹499.

### Product 4 — Accessories

- Premium accessories image.
- Product name and description.
- Star rating.
- Price: ₹899.

Product card requirements:

- Use separate, relevant images.
- Maintain consistent image dimensions.
- Display product name, description, rating, and price.
- Use gold-colored rating stars.
- Add subtle image zoom on hover.
- Include a functional product-details action.
- Load product information from Django models and MySQL.
- Treat the supplied prices as initial sample data.

## Benefits Grid

Display four benefits in a responsive grid.

1. **Free Shipping** — On orders above ₹999.
2. **Easy Returns** — 15 days return policy.
3. **Secure Payment** — Safe and secure checkout.
4. **24/7 Support** — We're here to help you.

Use clean icons, consistent spacing, and an elegant visual style.

## Footer

Create a reusable footer with four sections.

### MAX VIEW

"Premium fashion bringing modern trends with uncompromising quality and style."

### Shop

- New Arrivals
- Best Sellers
- Exclusive Offers
- Gift Cards

### Support

- Shipping Info
- Returns & Exchanges
- Size Guide
- Contact Us

### Newsletter

"Subscribe to receive updates, access to exclusive deals, and more."

Include an email input and Subscribe button with appropriate validation and backend handling.

Copyright:
"© 2026 MAX VIEW — All Rights Reserved."

Ensure footer links work correctly and avoid unnecessary dead links.

# PAGE 2 — CATEGORIES

Create a dedicated product category page.

## Four Categories

- Men's Wear.
- Women's Wear.
- Kids' Wear.
- Accessories.

## Category Functionality

- Clicking a category displays the corresponding products.
- Show the selected category heading.
- Do not mix unrelated category products.
- Allow users to switch between categories easily.

## Horizontal Image Slider

- Display fashion images sliding from left to right.
- Include previous and next controls.
- Support horizontal touch swiping on mobile.
- Use smooth transitions.
- Add subtle hover zoom.
- Prevent unwanted page overflow.

## Category Product Cards

Display product image, name, description, star rating, price, and relevant product actions.

Use Django models for categories and products. Reuse the common navbar and footer.

# PAGE 3 — ABOUT US

## Heading

ABOUT US

## Brand Story

"Max Collection was founded with a passion for fashion and a commitment to delivering quality, style, and affordability in one place. Our brand represents modern trends combined with timeless designs, making fashion accessible for everyone.

At Max Collection, we carefully curate a wide range of clothing and accessories that reflect elegance, comfort, and confidence. From everyday essentials to statement pieces, our collections are designed to suit every occasion and lifestyle."

## Our Mission

"Our mission at Max Collection is to inspire confidence through fashion by offering premium-quality products, exceptional value, and a seamless shopping experience. We strive to keep our customers stylish, comfortable, and satisfied at every step."

## Design Requirements

- Use a premium fashion image.
- Create a clean, elegant layout.
- Use readable typography and balanced spacing.
- Add subtle hover effects.
- Maintain the common navbar and footer.
- Ensure responsive behavior.

Preserve the supplied brand wording unless a change is approved.

# PAGE 4 — CONTACT US

## Contact Information

Display a store image and the following supplied details:

- Address: 123@ Tirupur, Tamil Nadu, Old Bus Stand Tirupur, INDIA.
- Telephone: 1234567890.
- Email: [maxview1@gmail.com](mailto\:maxview1@gmail.com).

Treat these details as unverified input and make them easy to update.

## Careers Section

Heading: Careers at Forever.

Description:
"Learn more about our teams and job openings."

Button: Explore Jobs.

Do not invent a job-listing system. Make the destination configurable if a careers page is not implemented.

## Send Us a Message

Create a form containing:

- Name.
- Email.
- Subject.
- Message.
- Send Message button.

Requirements:

- Validate required fields and email format.
- Handle successful and failed submissions.
- Provide clear feedback to the user.
- Store messages in the database or send them through a configured backend.
- Use Django CSRF protection and server-side validation.

Reuse the common footer.

# PAGE 5 — LOGIN AND REGISTRATION

## Login Page

- Username or email.
- Password.
- Login button.
- Registration link.
- Clear error messages.

## Registration Page

- Name.
- Email.
- Username.
- Password.
- Confirm password.
- Register button.

## Authentication

- Use Django Authentication.
- Store passwords securely using Django's password hashing.
- Implement secure login and logout.
- Protect authenticated features.
- Display the appropriate Login or Logout option in the navbar.

# ADDITIONAL FUNCTIONAL REQUIREMENTS

## Search

- Search products by name and relevant keywords.
- Display matching results.
- Show an appropriate message when no products match.
- Provide a way to return to the full product list.

## Shopping Cart

- Add products to cart.
- Update quantities.
- Remove items.
- Display subtotal and total.
- Maintain cart data appropriately using sessions and/or database storage.
- Validate prices and quantities on the server.
- Do not implement real payment processing without approval.

## Product Management

Create appropriate Django models for:

- Product.
- Category.
- Product image.
- Price.
- Description.
- Rating data where available.
- Stock quantity if inventory management is included.

Store application data in MySQL.

# DESIGN SYSTEM

## Color Palette

- Premium Black: #171717
- Deep Charcoal: #262626
- Champagne Gold: #D9A441
- Cream: #FFF4DC
- White: #FFFFFF
- Soft Neutral: #F7F5F0

## Visual Style

- Simple and luxurious.
- High-quality fashion photography.
- Elegant typography.
- Consistent spacing.
- Clean product cards.
- Subtle hover animations.
- Smooth transitions.
- Accessible forms and navigation.
- Responsive desktop, tablet, and mobile layouts.

Avoid clutter, excessive animations, oversized elements, and inconsistent styling.

# TECHNICAL REQUIREMENTS

- Use Django views and URL patterns.
- Create a reusable base.html template.
- Create reusable navbar and footer partials.
- Use Django template inheritance.
- Configure Tailwind CSS correctly for Django templates.
- Keep JavaScript in appropriate static files.
- Create models and migrations.
- Configure MySQL securely.
- Configure static and media file handling.
- Use environment variables for secrets and database credentials.
- Implement CSRF protection and server-side validation.
- Avoid duplicated templates and hardcoded duplicate product data.

# ACCEPTANCE CRITERIA

1. All five primary page types work correctly.
2. Navbar and footer are consistent across pages.
3. All navigation links point to appropriate destinations.
4. Home page displays the hero section, four product cards, benefits grid, and footer.
5. Category selection displays the correct products.
6. Image sliders work with controls and touch interactions.
7. Search returns relevant products.
8. Authentication works correctly.
9. Cart add, update, remove, and total calculations work correctly.
10. Contact and newsletter forms have appropriate backend handling.
11. Images load correctly without broken paths.
12. MySQL stores application data.
13. The website works on mobile, tablet, and desktop.
14. No unnecessary existing functionality is removed.
15. No real payment processing is added without approval.

# BMAD WORKFLOW

Follow these phases in order:

1. Requirements analysis.
2. Brainstorming and assumptions.
3. PRD creation.
4. Technical architecture.
5. Database design.
6. User stories and acceptance criteria.
7. Implementation planning.
8. Incremental implementation.
9. Functional and security testing.
10. Responsive testing and bug fixing.

Organize documentation in appropriate `_bmad-output/` folders, including `brainstorming/`, `prds/`, `architecture/`, `database/`, `documentation/`, `security/`, and `user-stories/`.

Generate the PRD and architecture first. Review them before implementation begins.

## Final Goal

Deliver a complete, responsive, premium MAX VIEW fashion e-commerce website using Django, HTML Templates, Tailwind CSS, JavaScript, and MySQL, implementing all specified pages and functionality.
