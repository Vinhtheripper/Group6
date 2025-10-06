const tabs = document.querySelectorAll(".tab-btn");
    const forms = document.querySelectorAll(".auth-form");

    function switchTab(tab) {
      tabs.forEach(t => t.classList.remove("active"));
      forms.forEach(f => f.style.display = "none");

      document.querySelector(`[data-tab=${tab}]`).classList.add("active");
      document.getElementById(tab).style.display = "block";
    }

    tabs.forEach(btn => {
      btn.addEventListener("click", () => switchTab(btn.dataset.tab));
    });