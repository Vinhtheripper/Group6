document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("container");
  const toggleRegisterBtn = document.getElementById("toggle-register");
  const toggleLoginBtn = document.getElementById("toggle-login");

  if (!container) {
    console.error("❌ Không tìm thấy phần tử #container");
    return;
  }

  if (toggleRegisterBtn) {
    toggleRegisterBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("👉 Click Sign Up");
      container.classList.add("active");
    });
  }

  if (toggleLoginBtn) {
    toggleLoginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("👉 Click Sign In");
      container.classList.remove("active");
    });
  }
});