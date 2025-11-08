document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".add-to-cart-form").forEach(form => {
    const dec = form.querySelector(".qty-decrease");
    const inc = form.querySelector(".qty-increase");
    const display = form.querySelector(".qty-display");
    const input = form.querySelector(".qty-input");

    let quantity = parseInt(input.value) || 1;

    function updateQty(newQty) {
      quantity = Math.max(1, newQty);
      display.textContent = quantity;
      input.value = quantity;
    }

    dec.addEventListener("click", (e) => {
      e.preventDefault();
      updateQty(quantity - 1);
    });

    inc.addEventListener("click", (e) => {
      e.preventDefault();
      updateQty(quantity + 1);
    });
  });
});

// Handle copying voucher codes
document.addEventListener('DOMContentLoaded', function () {
  const copyButtons = document.querySelectorAll('.btn-copy-code');

  copyButtons.forEach(button => {
    button.addEventListener('click', function () {
      const code = this.getAttribute('data-code');

      
      const textarea = document.createElement('textarea');
      textarea.value = code;
      document.body.appendChild(textarea);

      
      textarea.select();
      try {
        const successful = document.execCommand('copy');
        if (successful) {
          
          const originalText = this.innerHTML;
          this.innerHTML = '<i class="lni lni-checkmark"></i><span>Copied!</span>';

          
          setTimeout(() => {
            this.innerHTML = originalText;
          }, 2000);
        }
      } catch (err) {
        console.error('Failed to copy code:', err);
      }
      document.body.removeChild(textarea);
    });
  });
});


