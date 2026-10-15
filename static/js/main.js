/**
 * MAX VIEW Luxury Fashion E-Commerce Main Interactions
 */

// 1. Page Refresh & Load Behavior: Always scroll to top across all pages
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

window.addEventListener('beforeunload', function () {
    window.scrollTo(0, 0);
});

window.addEventListener('pageshow', function (event) {
    window.scrollTo(0, 0);
});

window.addEventListener('load', function () {
    // If user did not explicitly click an in-page anchor, always reset scroll position to top
    if (!window.location.hash) {
        window.scrollTo(0, 0);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // 2. Mobile Menu Drawer Toggling
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenuCloseBtn = document.getElementById('mobile-menu-close');
    const mobileMenuDrawer = document.getElementById('mobile-menu-drawer');
    const mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');

    function openMobileMenu() {
        if (mobileMenuDrawer && mobileMenuBackdrop) {
            mobileMenuDrawer.classList.remove('-translate-x-full');
            mobileMenuBackdrop.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeMobileMenu() {
        if (mobileMenuDrawer && mobileMenuBackdrop) {
            mobileMenuDrawer.classList.add('-translate-x-full');
            mobileMenuBackdrop.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openMobileMenu);
    }
    if (mobileMenuCloseBtn) {
        mobileMenuCloseBtn.addEventListener('click', closeMobileMenu);
    }
    if (mobileMenuBackdrop) {
        mobileMenuBackdrop.addEventListener('click', closeMobileMenu);
    }

    // 3. Desktop Categories Dropdown Click & Hover Handling
    // Clicking or hovering over Categories must NOT navigate to Men's Wear.
    // Clicking displays the 4 options: Men's Wear, Women's Wear, Kids' Wear, Accessories.
    const categoriesNavBtn = document.getElementById('categories-dropdown-btn');
    const categoriesDropdownMenu = document.getElementById('categories-dropdown-menu');

    if (categoriesNavBtn && categoriesDropdownMenu) {
        categoriesNavBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const isHidden = categoriesDropdownMenu.classList.contains('hidden');
            if (isHidden) {
                categoriesDropdownMenu.classList.remove('hidden');
                categoriesDropdownMenu.classList.remove('opacity-0', 'invisible');
                categoriesDropdownMenu.classList.add('opacity-100', 'visible');
            } else {
                categoriesDropdownMenu.classList.add('hidden');
                categoriesDropdownMenu.classList.add('opacity-0', 'invisible');
                categoriesDropdownMenu.classList.remove('opacity-100', 'visible');
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!categoriesNavBtn.contains(e.target) && !categoriesDropdownMenu.contains(e.target)) {
                categoriesDropdownMenu.classList.add('hidden');
                categoriesDropdownMenu.classList.add('opacity-0', 'invisible');
                categoriesDropdownMenu.classList.remove('opacity-100', 'visible');
            }
        });
    }

    // 4. Flash Messages Auto-Dismiss
    const messageToasts = document.querySelectorAll('.message-toast');
    messageToasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    });

    // 5. Escape Key handler
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMobileMenu();
            if (categoriesDropdownMenu) {
                categoriesDropdownMenu.classList.add('hidden');
            }
        }
    });
});
