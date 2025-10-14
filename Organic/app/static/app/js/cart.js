document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".qty-control").forEach(control => {
    const dec = control.querySelector(".cart-decrease");
    const inc = control.querySelector(".cart-increase");
    const display = control.querySelector(".cart-qty");
    const itemId = control.dataset.item;

    if (!display) return;
    let quantity = parseInt(display.textContent) || 1;

    function updateQty(newQty) {
      quantity = Math.max(1, newQty);
      display.textContent = quantity;

      // (Django view update_quantity)
      fetch(`/cart/update/${itemId}/${newQty > quantity ? "increase" : "decrease"}/`)
        .then(() => location.reload());
    }

    dec.addEventListener("click", () => updateQty(quantity - 1));
    inc.addEventListener("click", () => updateQty(quantity + 1));
  });
});
document.querySelectorAll(".remove-item").forEach(button => {
  button.addEventListener("click", function () {
    const itemId = this.dataset.item;
    fetch(`/cart/remove/${itemId}/`)
      .then(() => location.reload());
  });
});