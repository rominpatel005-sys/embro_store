/**
 * Faction Store - Premium Luxury UX Engines
 * Vanilla JavaScript implementation for high performance and premium animations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize UX modules
    initPreloader();
    initCustomCursor();
    initCanvasParticles();
    initHeroSlider();
    initTypingAnimation();
    initSpotlightEffect();
    initCounters();
    initBackToTop();
    initThemeToggle();
    initAJAXSearch();
    initAJAXCart();
    initAJAXWishlist();
    initScrollReveal();
    initStars();
});

// 1. Preloader Screen
function initPreloader() {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('fade-out');
            }, 600);
        });
        
        // Safety timeout in case load event already fired
        setTimeout(() => {
            if (!preloader.classList.contains('fade-out')) {
                preloader.classList.add('fade-out');
            }
        }, 3000);
    }
}

// 2. Custom Dual Cursor
function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    const dot = document.querySelector('.custom-cursor-dot');
    
    if (cursor && dot) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            
            dot.style.left = e.clientX + 'px';
            dot.style.top = e.clientY + 'px';
        });

        // Hover scale effects on interactive items
        const clickables = document.querySelectorAll('a, button, .btn, input, select, textarea, .product-wishlist-btn');
        clickables.forEach(item => {
            item.addEventListener('mouseenter', () => {
                cursor.style.width = '40px';
                cursor.style.height = '40px';
                cursor.style.backgroundColor = 'rgba(212, 175, 55, 0.1)';
            });
            item.addEventListener('mouseleave', () => {
                cursor.style.width = '20px';
                cursor.style.height = '20px';
                cursor.style.backgroundColor = 'transparent';
            });
        });
    }
}

// 3. Canvas Floating Particles
function initCanvasParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particlesArray = [];
    const numberOfParticles = 65;

    // Set dimensions
    function setCanvasSize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);

    // Particle constructor
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = Math.random() * 0.4 - 0.2;
            this.speedY = Math.random() * 0.4 - 0.2;
            this.color = 'rgba(212, 175, 55, 0.15)';
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Screen wrap around
            if (this.x > canvas.width) this.x = 0;
            else if (this.x < 0) this.x = canvas.width;
            
            if (this.y > canvas.height) this.y = 0;
            else if (this.y < 0) this.y = canvas.height;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }

    // Populate particles array
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }

    // Connect particles with web lines
    function connectParticles() {
        let opacityValue = 1;
        for (let a = 0; a < particlesArray.length; a++) {
            for (let b = a; b < particlesArray.length; b++) {
                let distSq = ((particlesArray[a].x - particlesArray[b].x) ** 2) + 
                             ((particlesArray[a].y - particlesArray[b].y) ** 2);
                
                // Draw line if close enough
                if (distSq < 15000) {
                    opacityValue = 1 - (distSq / 15000);
                    ctx.strokeStyle = `rgba(212, 175, 55, ${opacityValue * 0.06})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    // Loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
        }
        connectParticles();
        requestAnimationFrame(animate);
    }
    animate();
}

// 4. Auto Slider for Hero Section
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    if (slides.length > 0) {
        let currentSlide = 0;
        const slideInterval = 5000; // 5 seconds

        function nextSlide() {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }

        // Initialize first slide as active
        slides[0].classList.add('active');
        setInterval(nextSlide, slideInterval);
    }
}

// 5. Typing Text Animation
function initTypingAnimation() {
    const typingSpan = document.querySelector('.typing-text');
    if (typingSpan) {
        const words = ["PREMIUM APPARELS", "MODERN GENERATION STYLE", "STREETWEAR INSPIRED", "LUXURY FOOTWEAR", "TIMELESS DESIGNS"];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeSpeed = 150;

        function type() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                typingSpan.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 75; // Deletes faster
            } else {
                typingSpan.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 150;
            }

            if (!isDeleting && charIndex === currentWord.length) {
                typeSpeed = 2000; // Pause at the end of word
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeSpeed = 500; // Pause before typing new word
            }

            setTimeout(type, typeSpeed);
        }

        type();
    }
}

// 6. Spotlight Mouse Glow Effect
function initSpotlightEffect() {
    const spotlightCards = document.querySelectorAll('.spotlight-card');
    spotlightCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// 7. Statistics Animated Counters
function initCounters() {
    const counters = document.querySelectorAll('.counter-number');
    if (counters.length === 0) return;

    const countOptions = {
        root: null,
        threshold: 0.5,
        rootMargin: "0px"
    };

    const countObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const limit = parseInt(target.getAttribute('data-target'), 10);
                const suffix = target.getAttribute('data-suffix') || '';

                if (isNaN(limit) || limit <= 0) {
                    target.textContent = '0' + suffix;
                    observer.unobserve(target);
                    return;
                }

                let current = 0;
                const duration = 1500; // 1.5 seconds animation
                const increment = limit / (duration / 16); // 60 FPS approx

                function updateCount() {
                    current += increment;
                    if (current >= limit) {
                        target.textContent = limit + suffix;
                    } else {
                        target.textContent = Math.floor(current) + suffix;
                        requestAnimationFrame(updateCount);
                    }
                }
                updateCount();
                observer.unobserve(target);
            }
        });
    }, countOptions);

    counters.forEach(counter => {
        countObserver.observe(counter);
    });
}

// 8. Back to Top Button
function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    if (btn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                btn.classList.add('show');
            } else {
                btn.classList.remove('show');
            }
        });
        btn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// 9. Light/Dark Theme Switcher
function initThemeToggle() {
    const toggleBtn = document.querySelector('.theme-toggle-btn');
    if (toggleBtn) {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateToggleIcon(toggleBtn, savedTheme);

        toggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateToggleIcon(toggleBtn, newTheme);
            showToast(`Theme switched to ${newTheme} mode!`, 'info');
        });
    }
}

function updateToggleIcon(btn, theme) {
    const icon = btn.querySelector('i');
    if (icon) {
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
}

// 10. Toast Notifications Engine
function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    
    // Choose icon
    let iconClass = 'fa-check-circle';
    if (type === 'error') iconClass = 'fa-exclamation-triangle';
    if (type === 'info') iconClass = 'fa-info-circle';

    toast.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <i class="fas ${iconClass}"></i>
            <span>${message}</span>
        </div>
        <button class="btn-close btn-close-white ms-3" style="font-size: 0.75rem;" onclick="this.parentElement.remove()"></button>
    `;

    container.appendChild(toast);
    
    // Trigger entrance transition
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // Auto dismiss
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 500);
    }, 4000);
}

// 11. AJAX Live Catalog Search
function initAJAXSearch() {
    const searchInput = document.getElementById('search-input');
    const dropdown = document.getElementById('search-results-dropdown');
    
    if (searchInput && dropdown) {
        let debounceTimer;
        
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            clearTimeout(debounceTimer);
            
            if (query.length < 2) {
                dropdown.innerHTML = '';
                dropdown.classList.remove('active');
                return;
            }
            
            debounceTimer = setTimeout(() => {
                fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        dropdown.innerHTML = '';
                        if (data.results && data.results.length > 0) {
                            data.results.forEach(product => {
                                const item = document.createElement('a');
                                item.className = 'search-result-item';
                                item.href = `/product/${product.slug}/`;
                                item.innerHTML = `
                                    <img src="${product.image_url}" alt="${product.name}" class="search-result-img">
                                    <div class="search-result-info">
                                        <div class="search-result-name">${product.name}</div>
                                        <div class="search-result-brand">${product.brand}</div>
                                    </div>
                                    <div class="search-result-price">$${product.price}</div>
                                `;
                                dropdown.appendChild(item);
                            });
                            dropdown.classList.add('active');
                        } else {
                            dropdown.innerHTML = '<div class="p-3 text-muted text-center" style="font-size:0.9rem;">No products found</div>';
                            dropdown.classList.add('active');
                        }
                    })
                    .catch(err => console.error("Search AJAX error:", err));
            }, 300);
        });
        
        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    }
}

// 12. AJAX Add to Cart & Update Quantity
function initAJAXCart() {
    // Intercept standard cart submit forms
    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (form.classList.contains('ajax-cart-form')) {
            e.preventDefault();
            const url = form.getAttribute('action');
            const formData = new FormData(form);
            
            // Get CSRF Token
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    // Update header cart badge counts
                    updateCartBadges(data.cart_count);
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(err => {
                console.error("Cart action error:", err);
                showToast("Failed to update cart. Please try again.", "error");
            });
        }
    });
}

function updateCartBadges(count) {
    const badges = document.querySelectorAll('.cart-count-badge');
    badges.forEach(badge => {
        badge.textContent = count;
        if (count > 0) {
            badge.style.display = 'inline-block';
            badge.classList.add('animate-bounce'); // add micro animation
            setTimeout(() => badge.classList.remove('animate-bounce'), 800);
        } else {
            badge.style.display = 'none';
        }
    });
}

// 13. AJAX Wishlist Toggle
function initAJAXWishlist() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.ajax-wishlist-toggle');
        if (btn) {
            e.preventDefault();
            const url = btn.getAttribute('href') || btn.getAttribute('data-url');
            if (!url) return;
            
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => {
                if (res.status === 403 || res.redirected) {
                    // Unauthorized: redirect to login
                    window.location.href = '/accounts/login/';
                    return;
                }
                return res.json();
            })
            .then(data => {
                if (data && data.success) {
                    showToast(data.message, 'success');
                    
                    // Toggle Active classes
                    if (data.added) {
                        btn.classList.add('active');
                        const icon = btn.querySelector('i');
                        if (icon) icon.className = 'fas fa-heart text-danger';
                    } else {
                        btn.classList.remove('active');
                        const icon = btn.querySelector('i');
                        if (icon) icon.className = 'far fa-heart';
                        
                        // If we are on the wishlist detail page, dynamically prune the row
                        const wishlistItemRow = btn.closest('.wishlist-item-row');
                        if (wishlistItemRow) {
                            wishlistItemRow.style.opacity = '0';
                            setTimeout(() => {
                                wishlistItemRow.remove();
                                if (document.querySelectorAll('.wishlist-item-row').length === 0) {
                                    location.reload(); // Reload to show Empty Wishlist screen
                                }
                            }, 500);
                        }
                    }
                    
                    // Update header wishlist badge counts
                    updateWishlistBadges(data.wishlist_count);
                }
            })
            .catch(err => console.error("Wishlist AJAX error:", err));
        }
    });
}

function updateWishlistBadges(count) {
    const badges = document.querySelectorAll('.wishlist-count-badge');
    badges.forEach(badge => {
        badge.textContent = count;
        if (count > 0) {
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    });
}

// 14. Scroll Reveal Engine
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if (revealElements.length === 0) return;

    // Set simple initial CSS rules dynamically for safety
    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
    });

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
                observer.unobserve(el);
            }
        });
    }, {
        root: null,
        threshold: 0.15
    });

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
}

// 15. Star Width Applicator (to prevent inline style syntax linting warnings)
function initStars() {
    const stars = document.querySelectorAll('.stars-inner');
    stars.forEach(star => {
        const width = star.getAttribute('data-width');
        if (width) {
            star.style.width = width + '%';
        }
    });
}

