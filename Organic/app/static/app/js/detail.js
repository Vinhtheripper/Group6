
document.addEventListener("DOMContentLoaded", function () {
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const target = this.dataset.tab;


            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));


            this.classList.add("active");
            document.getElementById(target).classList.add("active");
        });
    });
});

// Image slider
document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".slide");
    const thumbs = document.querySelectorAll(".thumbnails img");
    let index = 0;
    let timer; // để quản lý setTimeout

    function showSlide(i) {
        if (!slides[i] || !thumbs[i]) return;
        slides.forEach(s => s.classList.remove("active"));
        thumbs.forEach(t => t.classList.remove("active"));
        slides[i].classList.add("active");
        thumbs[i].classList.add("active");
        index = i;

        resetAutoSlide(); // reset khi đổi ảnh
    }

    function autoSlide() {
        let next = (index + 1) % slides.length;
        showSlide(next);
    }

    function resetAutoSlide() {
        clearTimeout(timer);              // xóa timer cũ
        timer = setTimeout(autoSlide, 4000); // đặt lại sau 4s
    }

    // click thumbnail → đổi slide & reset auto slide
    thumbs.forEach((t, i) => {
        t.addEventListener("click", () => showSlide(i));
    });

    // bắt đầu auto slide lần đầu
    resetAutoSlide();
});


