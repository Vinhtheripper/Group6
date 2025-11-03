// Navigation handler
document.addEventListener('DOMContentLoaded', function () {
    // Xử lý các nút điều hướng
    const navLinks = {
        'home': 'index.html',
        'about': 'about.html',
        'products': 'Product_list.html',
        'blog': 'blog.html',
        'contact': 'contact.html',
        'cart': 'cart.html',
        'login': 'login.html',
        'checkout': 'checkout.html',
        'profile': 'profile.html'
    };

    // Thêm event listener cho tất cả các nút navigation
    Object.keys(navLinks).forEach(key => {
        const elements = document.querySelectorAll(`[data-nav="${key}"], .nav-${key}, #${key}-btn`);
        elements.forEach(element => {
            element.addEventListener('click', function (e) {
                e.preventDefault();
                window.location.href = navLinks[key];
            });
        });
    });

    // Xử lý nút "Xem chi tiết sản phẩm"
    const productDetailBtns = document.querySelectorAll('.product-detail-btn, .view-product');
    productDetailBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.dataset.productId || '1';
            window.location.href = `product-detail.html?id=${productId}`;
        });
    });

    // Xử lý nút "Thêm vào giỏ hàng"
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            // Logic thêm vào giỏ hàng
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
});

// Hàm thêm sản phẩm vào giỏ hàng
function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push(productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Đã thêm vào giỏ hàng!');
}

// Profile Page Functionality
document.addEventListener('DOMContentLoaded', function () {
    // Tab navigation
    document.querySelectorAll('.profile-navigation .nav-item').forEach(item => {
        item.addEventListener('click', function (e) {
            if (this.classList.contains('logout')) return;
            e.preventDefault();

            // Update navigation active state
            document.querySelectorAll('.profile-navigation .nav-item').forEach(nav => {
                nav.classList.remove('active');
            });
            this.classList.add('active');

            // Show corresponding section
            const sectionId = this.getAttribute('data-section');
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active');
        });
    });

    // Modal handling
    const modals = {
        editProfile: document.getElementById('editProfileModal'),
        changeAvatar: document.getElementById('changeAvatarModal'),
        changePassword: document.getElementById('changePasswordModal'),
        orderDetail: document.getElementById('orderDetailModal')
    };

    // Open modals
    if (document.getElementById('editProfileBtn')) {
        document.getElementById('editProfileBtn').addEventListener('click', () => {
            modals.editProfile.classList.add('active');
        });
    }

    if (document.getElementById('changeAvatarBtn')) {
        document.getElementById('changeAvatarBtn').addEventListener('click', () => {
            modals.changeAvatar.classList.add('active');
        });
    }

    if (document.getElementById('changePasswordBtn')) {
        document.getElementById('changePasswordBtn').addEventListener('click', () => {
            modals.changePassword.classList.add('active');
        });
    }

    // Close modals
    document.querySelectorAll('.modal .close-btn, .modal .cancel-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            this.closest('.modal').classList.remove('active');
        });
    });

    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', function () {
            if (this.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        });
    }

    // Avatar upload preview
    const avatarUpload = document.getElementById('avatarUpload');
    if (avatarUpload) {
        avatarUpload.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    document.getElementById('avatarPreview').src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Form submissions with toast notifications
    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', function (e) {
            e.preventDefault();
            // Here you would typically send the data to the server

            // Close the modal
            modals.editProfile.classList.remove('active');

            // Show success toast
            const toast = document.querySelector('.toast.success');
            toast.classList.add('active');

            // Auto hide toast after 3 seconds
            setTimeout(() => {
                toast.classList.remove('active');
            }, 3000);
        });
    }

    // Close toast on button click
    const toastClose = document.querySelector('.toast-close');
    if (toastClose) {
        toastClose.addEventListener('click', function () {
            this.closest('.toast').classList.remove('active');
        });
    }

    // Order detail tab functionality
    document.querySelectorAll('.tab-btn').forEach(tab => {
        tab.addEventListener('click', function () {
            // Remove active class from all tabs
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');

            // Get the tab ID
            const tabId = this.getAttribute('data-tab');

            // Hide all panels
            document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));

            // Show corresponding panel
            document.getElementById(tabId + '-panel').classList.add('active');
        });
    });
});

// === ORDER HISTORY: View Details === //
        document.querySelectorAll('#orders .btn-details').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                document.getElementById('orderDetailModal').classList.add('active');
            });
        });

        // === AI MENU HISTORY: View Details === //
        document.querySelectorAll('#ai-menu-history .btn-details').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                document.getElementById('aiMenuDetailModal').classList.add('active');
            });
        });

        // === Đóng tất cả modal khi bấm nút close === //
        document.querySelectorAll('.modal .close-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                this.closest('.modal').classList.remove('active');
            });
        });

        // === (Tùy chọn) Đóng modal khi click ngoài nội dung === //
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function (e) {
                if (e.target === this) {
                    this.classList.remove('active');
                }
            });
        });

        