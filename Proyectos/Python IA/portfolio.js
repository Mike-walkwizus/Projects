// ============ PARTICLE SYSTEM ============
class Particle {
    constructor(canvas) {
        this.canvas = canvas;
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.color = ['#6366f1', '#ec4899', '#10b981', '#f59e0b'][Math.floor(Math.random() * 4)];
        this.opacity = Math.random() * 0.5 + 0.3;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        
        if (this.x > this.canvas.width) this.x = 0;
        if (this.x < 0) this.x = this.canvas.width;
        if (this.y > this.canvas.height) this.y = 0;
        if (this.y < 0) this.y = this.canvas.height;
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.opacity;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
}

let particles = [];
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

function initParticles() {
    particles = [];
    for (let i = 0; i < 50; i++) {
        particles.push(new Particle(canvas));
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
        particle.update();
        particle.draw(ctx);
    });
    
    requestAnimationFrame(animateParticles);
}

resizeCanvas();
initParticles();
animateParticles();

window.addEventListener('resize', () => {
    resizeCanvas();
    initParticles();
});

// ============ MOUSE TRAIL EFFECT ============
const mouseTrailContainer = document.getElementById('mouseTrail');
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    // Create trail dots randomly
    if (Math.random() > 0.85) {
        const dot = document.createElement('div');
        dot.className = 'trail-dot';
        dot.style.left = (mouseX + Math.random() * 20 - 10) + 'px';
        dot.style.top = (mouseY + Math.random() * 20 - 10) + 'px';
        mouseTrailContainer.appendChild(dot);
        
        setTimeout(() => {
            dot.remove();
        }, 600);
    }
});

// ============ DARK MODE TOGGLE ============
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;
let isDarkMode = localStorage.getItem('darkMode') === 'true';

function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    updateThemeIcon();
}

function updateThemeIcon() {
    themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
}

if (isDarkMode) {
    document.body.classList.add('dark-mode');
}
updateThemeIcon();

themeToggle.addEventListener('click', toggleDarkMode);

// ============ MOBILE MENU TOGGLE ============
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    
    const spans = hamburger.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(8px, 8px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(7px, -7px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
});

const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const spans = hamburger.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    });
});

// ============ SMOOTH SCROLLING ============
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============ NAVBAR SCROLL EFFECT ============
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.background = isDarkMode 
            ? 'rgba(15, 23, 42, 0.98)' 
            : 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.background = isDarkMode
            ? 'rgba(15, 23, 42, 0.95)'
            : 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// ============ INTERSECTION OBSERVER FOR ANIMATIONS ============
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.project-card, .skill-category, .stat').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    observer.observe(element);
});

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// ============ 3D FLIP CARDS ============
document.querySelectorAll('.flip-card').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('mouseenter', function() {
        this.style.filter = 'drop-shadow(0 10px 30px rgba(99, 102, 241, 0.4))';
    });
    card.addEventListener('mouseleave', function() {
        this.style.filter = 'drop-shadow(0 4px 20px rgba(0, 0, 0, 0.1))';
    });
});

// ============ FORM HANDLING ============
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const inputs = contactForm.querySelectorAll('input, textarea');
        const formValues = {
            name: inputs[0].value,
            email: inputs[1].value,
            message: inputs[2].value
        };

        if (!formValues.name || !formValues.email || !formValues.message) {
            showNotification('Please fill in all fields', 'error');
            return;
        }

        if (!isValidEmail(formValues.email)) {
            showNotification('Please enter a valid email', 'error');
            return;
        }

        const submitButton = contactForm.querySelector('button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;

        setTimeout(() => {
            showNotification('Message sent successfully! I\'ll get back to you soon.', 'success');
            contactForm.reset();
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }, 1500);
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 2000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

const slideStyle = document.createElement('style');
slideStyle.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(slideStyle);

// ============ PARALLAX EFFECT ============
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.floating-box, .floating-circle, .floating-triangle, .image-placeholder');
    
    parallaxElements.forEach((element, index) => {
        element.style.transform = `translateY(${scrolled * (0.5 - index * 0.05)}px)`;
    });
});

// ============ COUNTER ANIMATION ============
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

const stats = document.querySelectorAll('.stat h3');
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const text = entry.target.textContent;
            const number = parseInt(text);
            if (!isNaN(number)) {
                animateCounter(entry.target, number);
                statsObserver.unobserve(entry.target);
            }
        }
    });
}, { threshold: 0.5 });

stats.forEach(stat => statsObserver.observe(stat));

// ============ ACTIVE NAV LINK ON SCROLL ============
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.style.borderBottomColor = 'var(--primary-color)';
        } else {
            link.style.borderBottomColor = 'transparent';
        }
    });
});

// ============ KEYBOARD NAVIGATION ============
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        const spans = hamburger.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
});

// ============ PROJECT CARD HOVER EFFECT ============
const projectCards = document.querySelectorAll('.project-card');
projectCards.forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('mouseenter', () => {
        projectCards.forEach(c => {
            if (c !== card) {
                c.style.opacity = '0.7';
            }
        });
    });
    card.addEventListener('mouseleave', () => {
        projectCards.forEach(c => {
            c.style.opacity = '1';
        });
    });
});

// ============ 3D TOUCHSCREEN SUPPORT ============
let deviceOrientation = { alpha: 0, beta: 0, gamma: 0 };

if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', (event) => {
        deviceOrientation.alpha = event.alpha;
        deviceOrientation.beta = event.beta;
        deviceOrientation.gamma = event.gamma;
        
        const cube = document.querySelector('.cube');
        if (cube) {
            cube.style.transform = `rotateX(${deviceOrientation.beta}deg) rotateY(${deviceOrientation.gamma}deg)`;
        }
    });
}

// ============ ENHANCED ANIMATIONS ============
// Stagger animation for multiple elements
function staggerElements(selector, delay = 100) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * delay}ms`;
    });
}

staggerElements('.skill-item', 50);
staggerElements('.project-card', 100);

// ============ PERFORMANCE OPTIMIZATION ============
// Reduce particle count on lower-end devices
if (window.innerWidth < 768) {
    particles = particles.slice(0, 25);
}

// ============ CONSOLE MESSAGE ============
console.log('%c✨ Welcome to Timanoki Portfolio! ✨', 'color: #6366f1; font-size: 20px; font-weight: bold;');
console.log('%cPowered by advanced CSS 3D transforms, particle systems, and smooth animations!', 'color: #ec4899; font-size: 14px;');

