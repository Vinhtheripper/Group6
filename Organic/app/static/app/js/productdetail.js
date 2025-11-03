document.addEventListener('DOMContentLoaded', function () {
    const mainImage = document.querySelector('.product-images .main-image');
    if (!mainImage) return;

    // Create floating thumbnail
    const floating = document.createElement('div');
    floating.className = 'floating-thumb';
    const img = document.createElement('img');
    img.src = mainImage.src;
    img.alt = mainImage.alt || '';
    floating.appendChild(img);
    document.body.appendChild(floating);

    // Observe main image visibility
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                floating.classList.remove('visible');
            } else {
                floating.classList.add('visible');
            }
        });
    }, { threshold: 0 });

    observer.observe(mainImage);

    // Update floating image when thumbnails are clicked
    document.querySelectorAll('.thumbnail').forEach(t => {
        t.addEventListener('click', () => {
            img.src = t.src;
        });
    });

    // Clicking floating thumb scrolls to main image
    floating.addEventListener('click', () => {
        mainImage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
});
