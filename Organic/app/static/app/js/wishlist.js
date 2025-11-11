window.addEventListener("beforeunload", () => {
    localStorage.setItem(location.pathname + "_scroll", window.scrollY);
});

window.addEventListener("load", () => {
    const key = location.pathname + "_scroll";
    const pos = localStorage.getItem(key);
    if (pos) {
        window.scrollTo(0, pos);
        localStorage.removeItem(key);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const wishlistBtns = document.querySelectorAll(".wishlist-btn");
    const wishlistContainer = document.querySelector(".wishlist-items");
    const wishlistCount = document.querySelector(".wishlist-count");

    // Lấy wishlist từ localStorage
    let wishlist = JSON.parse(localStorage.getItem("wishlist") || "[]");

    // Hàm render lại danh sách
    function renderWishlist() {
        wishlistContainer.innerHTML = "";

        if (wishlist.length === 0) {
            wishlistContainer.innerHTML = `<p class="empty-wishlist-msg">Your wishlist is empty</p>`;
            wishlistCount.textContent = "0";
            return;
        }

        wishlist.forEach(item => {
            const el = document.createElement("div");
            el.classList.add("wishlist-item");
            el.innerHTML = `
                <div class="wishlist-item-card">
                    <img src="${item.image}" alt="${item.name}">
                    <div class="item-info">
                    <p class="item-name">${item.name}</p>
                    <p class="item-price">$${item.price}</p>
                    </div>
                    <button class="remove-wish" data-id="${item.id}">✕</button>
                </div>
                `;

            wishlistContainer.appendChild(el);
        });

        wishlistCount.textContent = wishlist.length;
    }


    renderWishlist();


    wishlistBtns.forEach(btn => {
        const id = btn.dataset.id;

        // Nếu đã trong wishlist, hiển thị active
        if (wishlist.some(i => i.id === id)) btn.classList.add("active");

        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const product = {
                id: btn.dataset.id,
                name: btn.dataset.name,
                image: btn.dataset.image,
                price: btn.dataset.price
            };

            const index = wishlist.findIndex(i => i.id === product.id);

            if (index === -1) {
                wishlist.push(product);
                btn.classList.add("active");
            } else {
                wishlist.splice(index, 1);
                btn.classList.remove("active");
            }

            localStorage.setItem("wishlist", JSON.stringify(wishlist));
            renderWishlist();
        });
    });

    // Xử lý nút xóa trong dropdown
    wishlistContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-wish")) {
            const id = e.target.dataset.id;
            wishlist = wishlist.filter(i => i.id !== id);
            localStorage.setItem("wishlist", JSON.stringify(wishlist));
            renderWishlist();

            // Bỏ active trên nút ❤️ tương ứng
            const heart = document.querySelector(`.wishlist-btn[data-id="${id}"]`);
            if (heart) heart.classList.remove("active");
        }
    });
});

