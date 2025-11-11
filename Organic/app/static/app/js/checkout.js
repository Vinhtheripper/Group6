document.addEventListener("DOMContentLoaded", () => {
  const fields = ["address", "note"];

  // 1. Gán lại dữ liệu đã lưu
  fields.forEach(name => {
    const saved = sessionStorage.getItem(name);
    const el = document.querySelector(`[name="${name}"]`);
    if (saved && el) {
      el.value = saved;
    }
  });

  // 2. Lưu lại khi user nhập
  fields.forEach(name => {
    const el = document.querySelector(`[name="${name}"]`);
    if (el) {
      el.addEventListener("input", () => {
        sessionStorage.setItem(name, el.value);
      });
    }
  });

  // 3. Xóa cache khi bấm submit (đặt hàng)
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", (e) => {
      // nếu có nút name="placeorder" thì mới xóa
      const btn = e.submitter || document.activeElement;
      if (btn && btn.name === "placeorder") {
        fields.forEach(name => sessionStorage.removeItem(name));
      }
    });
  }

  // 4. Xử lý chọn phương thức thanh toán
  const radios = document.querySelectorAll('.payment-option input[type="radio"]');
  radios.forEach(radio => {
    radio.addEventListener('change', function () {
      document.querySelectorAll('.payment-option').forEach(opt => opt.classList.remove('selected'));
      const parent = this.closest('.payment-option');
      if (this.checked && parent) {
        parent.classList.add('selected');
      }
    });
  });
});