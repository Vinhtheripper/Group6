document.addEventListener('DOMContentLoaded', function () {

  const mainImage = document.querySelector('.product-images .main-image');
  if (mainImage) {
    const floating = document.createElement('div');
    floating.className = 'floating-thumb';
    const img = document.createElement('img');
    img.src = mainImage.src;
    img.alt = mainImage.alt || '';
    floating.appendChild(img);
    document.body.appendChild(floating);


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
    document.querySelectorAll('.thumbnail').forEach(t => {
      t.addEventListener('click', () => {
        const thumbImg = t.tagName === 'IMG' ? t : t.querySelector('img');
        if (thumbImg) {
          img.src = thumbImg.src;
          img.alt = thumbImg.alt || '';
        }
      });
    });

   
    floating.addEventListener('click', () => {
      mainImage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

 
  const tabs = document.querySelectorAll(".tab");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const target = document.getElementById(tab.dataset.tab);
      if (target) target.classList.add("active");
    });
  });
});
