document.addEventListener("DOMContentLoaded", () => {
  const fields = ["address", "note"];

  // 🔹 Gán lại dữ liệu đã lưu
  fields.forEach(name => {
    const saved = sessionStorage.getItem(name);
    if (saved) {
      const el = document.querySelector(`[name="${name}"]`);
      if (el) el.value = saved;
    }
  });

  // 🔹 Khi user nhập, lưu tạm vào sessionStorage
  fields.forEach(name => {
    const el = document.querySelector(`[name="${name}"]`);
    if (el) {
      el.addEventListener("input", () => {
        sessionStorage.setItem(name, el.value);
      });
    }
  });

  // 🔹 Khi bấm “Đặt hàng” → xóa cache
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", (e) => {
      if (e.submitter && e.submitter.name === "placeorder") {
        fields.forEach(name => sessionStorage.removeItem(name));
      }
    });
  }
});
