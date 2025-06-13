document.addEventListener('DOMContentLoaded', function() {
    // Hero Slider
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds

    function showSlide(n) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));

        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    // Auto slide
    let slideTimer = setInterval(nextSlide, slideInterval);

    // Manual controls
    document.querySelector('.prev-btn').addEventListener('click', function() {
        clearInterval(slideTimer);
        showSlide(currentSlide - 1);
        slideTimer = setInterval(nextSlide, slideInterval);
    });

    document.querySelector('.next-btn').addEventListener('click', function() {
        clearInterval(slideTimer);
        showSlide(currentSlide + 1);
        slideTimer = setInterval(nextSlide, slideInterval);
    });

    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', function() {
            clearInterval(slideTimer);
            showSlide(index);
            slideTimer = setInterval(nextSlide, slideInterval);
        });
    });

    // Quick View Modal
    const quickViewButtons = document.querySelectorAll('.quick-view');
    const modal = document.getElementById('quickViewModal');
    const closeModal = document.querySelector('.close-modal');

    quickViewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productCard = this.closest('.product-card');
            const productId = productCard.querySelector('.add-to-cart').getAttribute('data-product-id');

            // Here you would typically fetch product details via AJAX
            // For demo purposes, we'll just show the modal
            fetch(`/products/${productId}/quick-view/`)
                .then(response => response.text())
                .then(html => {
                    document.querySelector('.modal-body').innerHTML = html;
                    modal.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.querySelector('.modal-body').innerHTML = '<p>Error loading product details</p>';
                    modal.style.display = 'block';
                });
        });
    });

    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Add to Cart
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const cartCount = document.querySelector('.cart-count');

            // Here you would typically send an AJAX request to add to cart
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({quantity: 1})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count
                    cartCount.textContent = data.cart_count;
                    cartCount.style.display = 'flex';

                    // Show success message
                    alert('Product added to cart!');
                } else {
                    alert('Error adding product to cart');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding product to cart');
            });
        });
    });

    // Sort Products
    const sortSelect = document.getElementById('sort-products');

    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            window.location.href = `?sort=${sortValue}`;
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});