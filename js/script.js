// ========================================
// Mobile Menu Toggle
// ========================================

const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');

        // Animate hamburger icon
        const spans = mobileMenuToggle.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translateY(8px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            const spans = mobileMenuToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// ========================================
// Header Scroll Effect
// ========================================

const header = document.querySelector('.header');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        header.style.padding = '10px 0';
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
    } else {
        header.style.padding = '20px 0';
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }

    lastScroll = currentScroll;
});

// ========================================
// Smooth Scroll for Anchor Links
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        // Don't prevent default for # or #book (which might be handled elsewhere)
        if (href === '#' || href === '#book') {
            return;
        }

        e.preventDefault();
        const target = document.querySelector(href);

        if (target) {
            const headerHeight = header.offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ========================================
// Newsletter Form Handler
// ========================================

const newsletterForm = document.getElementById('newsletter-form');
const newsletterMessage = document.getElementById('newsletter-message');

if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const emailInput = newsletterForm.querySelector('input[type="email"]');
        const email = emailInput.value.trim();

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        // Simulate form submission
        // In a real application, this would send data to a server
        newsletterMessage.textContent = 'Subscribing...';
        newsletterMessage.className = 'newsletter-message';
        newsletterMessage.style.display = 'block';

        setTimeout(() => {
            showMessage('Thank you for subscribing! Check your email for confirmation.', 'success');
            emailInput.value = '';
        }, 1500);
    });
}

function showMessage(message, type) {
    newsletterMessage.textContent = message;
    newsletterMessage.className = `newsletter-message ${type}`;
    newsletterMessage.style.display = 'block';

    // Hide message after 5 seconds
    setTimeout(() => {
        newsletterMessage.style.display = 'none';
    }, 5000);
}

// ========================================
// Intersection Observer for Animations
// ========================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all service cards, pricing cards, and feature items
const animateElements = document.querySelectorAll('.service-card, .pricing-card, .feature-item, .stat-item');
animateElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// ========================================
// "Book Now" Button Handler
// ========================================

const bookButtons = document.querySelectorAll('a[href="#book"]');
bookButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();

        // You can customize this to open a booking modal or redirect to a booking page
        alert('Booking system would be integrated here.\n\nIn a production site, this would:\n• Open a booking modal\n• Redirect to a scheduling page\n• Connect to a booking API\n\nFor now, please call (555) 123-4567 to book your appointment!');
    });
});

// ========================================
// Dynamic Year in Footer
// ========================================

const footerYear = document.querySelector('.footer-content p');
if (footerYear && footerYear.textContent.includes('2024')) {
    const currentYear = new Date().getFullYear();
    footerYear.textContent = footerYear.textContent.replace('2024', currentYear);
}

// ========================================
// Page Load Animation
// ========================================

window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';

    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// ========================================
// Console Message
// ========================================

console.log('%c🌿 Shamrock Day Spa Website', 'color: #1B5971; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with care for your wellness journey', 'color: #FBBD48; font-size: 14px;');
