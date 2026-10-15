/**
 * MAX VIEW Lookbook Horizontal Slider
 * Supports mouse navigation controls and mobile touch swiping
 */

function initLookbookSlider(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const track = container.querySelector('.slider-track');
    const slides = container.querySelectorAll('.slider-slide');
    const prevBtn = container.querySelector('.slider-prev');
    const nextBtn = container.querySelector('.slider-next');
    const dots = container.querySelectorAll('.slider-dot');

    if (!track || slides.length === 0) return;

    let currentIndex = 0;
    const totalSlides = slides.length;
    let touchStartX = 0;
    let touchEndX = 0;

    function updateSlider(index) {
        if (index < 0) {
            currentIndex = totalSlides - 1;
        } else if (index >= totalSlides) {
            currentIndex = 0;
        } else {
            currentIndex = index;
        }

        const offsetPercentage = -(currentIndex * 100);
        track.style.transform = `translateX(${offsetPercentage}%)`;

        // Update dots
        dots.forEach((dot, idx) => {
            if (idx === currentIndex) {
                dot.classList.add('bg-luxury-gold', 'w-8');
                dot.classList.remove('bg-neutral-600', 'w-2');
            } else {
                dot.classList.remove('bg-luxury-gold', 'w-8');
                dot.classList.add('bg-neutral-600', 'w-2');
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => updateSlider(currentIndex - 1));
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => updateSlider(currentIndex + 1));
    }

    dots.forEach((dot, idx) => {
        dot.addEventListener('click', () => updateSlider(idx));
    });

    // Touch event listeners for mobile swiping
    track.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    track.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const threshold = 50; // Minimum px distance to register a swipe
        if (touchEndX < touchStartX - threshold) {
            // Swiped left -> next
            updateSlider(currentIndex + 1);
        } else if (touchEndX > touchStartX + threshold) {
            // Swiped right -> prev
            updateSlider(currentIndex - 1);
        }
    }

    // Initialize first slide
    updateSlider(0);
}

document.addEventListener('DOMContentLoaded', () => {
    initLookbookSlider('lookbook-slider');
});
