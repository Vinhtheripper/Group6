
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
