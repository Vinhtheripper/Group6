const farmData = {
  dalat: {
    photo: "https://picsum.photos/500/300?strawberry",
    name: "Nông trại Đà Lạt",
    cert: "VietGAP, USDA Organic",
    desc: "Trang trại trên cao nguyên Lâm Viên, khí hậu mát mẻ. Cung cấp rau quả hữu cơ như xà lách, cà chua bi, dâu tây."
  },
  longan: {
    photo: "https://picsum.photos/500/300?dragonfruit",
    name: "Nông trại Long An",
    cert: "GlobalGAP, Hữu cơ Việt Nam",
    desc: "Chuyên canh trái cây nhiệt đới như xoài, thanh long. Ứng dụng IoT kiểm soát tưới tiêu và đất."
  },
  lamdong: {
    photo: "https://picsum.photos/500/300?tomato",
    name: "Nông trại Lâm Đồng",
    cert: "VietGAP, JAS Organic",
    desc: "Hơn 50ha rau quả hữu cơ, ứng dụng công nghệ nhà kính và blockchain trong truy xuất nguồn gốc."
  }
};

const infoBox = document.getElementById("farmInfo");

document.querySelectorAll(".marker").forEach(m => {
  m.addEventListener("click", () => {
    const f = farmData[m.dataset.farm];
    infoBox.classList.add("hidden");
    setTimeout(() => {
      infoBox.innerHTML = `
            <img src="${f.photo}" class="farm-photo" alt="${f.name}">
            <div class="farm-body">
              <span class="badge">${f.cert}</span>
              <h2>${f.name}</h2>
              <p>${f.desc}</p>
              <a href="#" class="btn btn-primary">Xem chi tiết nông trại</a>
            </div>
          `;
      infoBox.classList.remove("hidden");
    }, 250);
  });
});