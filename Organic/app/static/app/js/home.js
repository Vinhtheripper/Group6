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
