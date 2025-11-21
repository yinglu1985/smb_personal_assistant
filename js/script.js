// ========================================
// Configuration
// ========================================

const API_BASE_URL = 'http://localhost:5001/api';

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

        // Don't prevent default for # or #book (handled by modal)
        if (href === '#' || href === '#book') {
            if (href === '#book') {
                e.preventDefault();
                openBookingModal();
            }
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
    newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = newsletterForm.querySelector('input[type="email"]');
        const email = emailInput.value.trim();

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            showNewsletterMessage('Please enter a valid email address.', 'error');
            return;
        }

        showNewsletterMessage('Subscribing...', 'loading');

        try {
            const response = await fetch(`${API_BASE_URL}/newsletter/subscribe`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok) {
                showNewsletterMessage(data.message || 'Thank you for subscribing!', 'success');
                emailInput.value = '';
            } else {
                showNewsletterMessage(data.error || 'Subscription failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Newsletter subscription error:', error);
            showNewsletterMessage('Network error. Please check your connection.', 'error');
        }
    });
}

function showNewsletterMessage(message, type) {
    newsletterMessage.textContent = message;
    newsletterMessage.className = `newsletter-message ${type}`;
    newsletterMessage.style.display = 'block';

    if (type !== 'loading') {
        setTimeout(() => {
            newsletterMessage.style.display = 'none';
        }, 5000);
    }
}

// ========================================
// Booking Modal
// ========================================

const bookingModal = document.getElementById('booking-modal');
const bookingForm = document.getElementById('booking-form');
const closeModalBtn = document.querySelector('.close-modal');
const bookingMessage = document.getElementById('booking-message');

let servicesData = [];

function openBookingModal() {
    bookingModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    loadServices();
}

function closeBookingModal() {
    bookingModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    bookingForm.reset();
    bookingMessage.style.display = 'none';
}

if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeBookingModal);
}

// Close modal when clicking outside
bookingModal?.addEventListener('click', (e) => {
    if (e.target === bookingModal) {
        closeBookingModal();
    }
});

// Load services from API
async function loadServices() {
    const serviceSelect = document.getElementById('service_id');

    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const services = await response.json();

        servicesData = services;

        serviceSelect.innerHTML = '<option value="">Select a service</option>';
        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = `${service.name} - $${service.price} (${service.duration_minutes} min)`;
            serviceSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load services:', error);
        serviceSelect.innerHTML = '<option value="">Failed to load services</option>';
    }
}

// Set minimum date to today
const dateInput = document.getElementById('date');
if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;

    // Load available time slots when date changes
    dateInput.addEventListener('change', loadAvailableTimeSlots);
}

// Load available time slots
async function loadAvailableTimeSlots() {
    const dateInput = document.getElementById('date');
    const timeSelect = document.getElementById('time');
    const serviceSelect = document.getElementById('service_id');

    const date = dateInput.value;
    const serviceId = serviceSelect.value;

    if (!date) {
        return;
    }

    timeSelect.innerHTML = '<option value="">Loading times...</option>';

    try {
        const url = new URL(`${API_BASE_URL}/appointments/available-slots`);
        url.searchParams.append('date', date);
        if (serviceId) {
            url.searchParams.append('service_id', serviceId);
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.slots && data.slots.length > 0) {
            timeSelect.innerHTML = '<option value="">Select a time</option>';
            data.slots.forEach(slot => {
                const option = document.createElement('option');
                option.value = slot.time;
                option.textContent = slot.display;
                timeSelect.appendChild(option);
            });
        } else {
            timeSelect.innerHTML = '<option value="">No slots available</option>';
        }
    } catch (error) {
        console.error('Failed to load time slots:', error);
        timeSelect.innerHTML = '<option value="">Failed to load times</option>';
    }
}

// Handle booking form submission
if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(bookingForm);
        const data = {
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            service_id: parseInt(formData.get('service_id')),
            date: formData.get('date'),
            time: formData.get('time'),
            notes: formData.get('notes') || ''
        };

        showBookingMessage('Booking your appointment...', 'loading');

        try {
            const response = await fetch(`${API_BASE_URL}/appointments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                showBookingMessage(
                    '✓ Appointment booked successfully! Check your email for confirmation.',
                    'success'
                );
                bookingForm.reset();

                // Close modal after 3 seconds
                setTimeout(() => {
                    closeBookingModal();
                }, 3000);
            } else {
                showBookingMessage(result.error || 'Booking failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Booking error:', error);
            showBookingMessage('Network error. Please check your connection and try again.', 'error');
        }
    });
}

function showBookingMessage(message, type) {
    bookingMessage.textContent = message;
    bookingMessage.className = `form-message ${type}`;
    bookingMessage.style.display = 'block';
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
console.log('%cBackend API: ' + API_BASE_URL, 'color: #666; font-size: 12px;');
