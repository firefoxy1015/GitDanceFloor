(() => {
  const data = window.CATALOG;

  // --- Render category grid -------------------------------------------------
  const grid = document.getElementById("cat-grid");
  data.categories.forEach((cat) => {
    const el = document.createElement("a");
    el.className = "cat-card reveal";
    el.id = cat.id;
    el.href = "#" + cat.id;
    el.dataset.cat = cat.id;
    el.innerHTML = `
      <div class="photo" style="background-image:url('${cat.cardImage}')"></div>
      <div class="body">
        <span class="tag">${cat.products.length} products</span>
        <h3>${cat.name}</h3>
        <p>${cat.tagline}</p>
        <div class="meta">
          <span>View product range</span>
          <span class="arrow" aria-hidden="true">→</span>
        </div>
      </div>`;
    el.addEventListener("click", (e) => {
      e.preventDefault();
      openDrawer(cat.id);
      history.replaceState(null, "", "#" + cat.id);
    });
    grid.appendChild(el);
  });

  // --- Drawer ---------------------------------------------------------------
  const drawer = document.getElementById("drawer");
  const backdrop = document.getElementById("drawer-backdrop");
  const drawerClose = document.getElementById("drawer-close");
  const drawerHero = document.getElementById("drawer-hero");
  const drawerTitle = document.getElementById("drawer-title");
  const drawerEyebrow = document.getElementById("drawer-eyebrow");
  const drawerSummary = document.getElementById("drawer-summary");
  const productList = document.getElementById("product-list");

  function openDrawer(catId) {
    const cat = data.categories.find((c) => c.id === catId);
    if (!cat) return;

    drawerEyebrow.textContent = cat.tagline;
    drawerTitle.textContent = cat.name;
    drawerHero.style.backgroundImage = `url('${cat.heroImage || cat.cardImage}')`;
    drawerSummary.textContent = cat.summary || "";

    productList.innerHTML = "";
    cat.products.forEach((p) => {
      const c = document.createElement("article");
      c.className = "prod-card";
      c.innerHTML = `
        <h4>${p.name}</h4>
        <div class="sub">${p.subtitle || ""}</div>
        <div class="arrow-row"><span>View details</span><span>→</span></div>`;
      c.addEventListener("click", () => openModal(cat, p));
      productList.appendChild(c);
    });

    drawer.classList.add("open");
    backdrop.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }
  function closeDrawer() {
    drawer.classList.remove("open");
    backdrop.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }
  drawerClose.addEventListener("click", closeDrawer);
  backdrop.addEventListener("click", closeDrawer);

  // --- Modal ----------------------------------------------------------------
  const modal = document.getElementById("modal");
  const modalBackdrop = document.getElementById("modal-backdrop");
  const modalClose = document.getElementById("modal-close");
  const modalPhoto = document.getElementById("modal-photo");
  const modalEyebrow = document.getElementById("modal-eyebrow");
  const modalTitle = document.getElementById("modal-title");
  const modalSub = document.getElementById("modal-sub");
  const modalDesc = document.getElementById("modal-desc");
  const modalSpecs = document.getElementById("modal-specs");
  const modalHighlightsWrap = document.getElementById("modal-highlights-wrap");

  function openModal(cat, p) {
    modalEyebrow.textContent = cat.name;
    modalTitle.textContent = p.name;
    modalSub.textContent = p.subtitle || "";
    modalDesc.textContent = p.description || "";
    modalPhoto.style.backgroundImage = `url('${p.image || cat.cardImage}')`;

    modalSpecs.innerHTML = "";
    (p.specs || []).forEach(([k, v]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${k}</td><td>${v}</td>`;
      modalSpecs.appendChild(tr);
    });

    modalHighlightsWrap.innerHTML = "";
    if (p.highlights && p.highlights.length) {
      const h = document.createElement("h3");
      h.textContent = "Highlights";
      const ul = document.createElement("ul");
      p.highlights.forEach((t) => {
        const li = document.createElement("li");
        li.textContent = t;
        ul.appendChild(li);
      });
      modalHighlightsWrap.appendChild(h);
      modalHighlightsWrap.appendChild(ul);
    }

    modal.classList.add("open");
    modalBackdrop.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }
  function closeModal() {
    modal.classList.remove("open");
    modalBackdrop.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }
  modalClose.addEventListener("click", closeModal);
  modalBackdrop.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (modal.classList.contains("open")) closeModal();
    else if (drawer.classList.contains("open")) closeDrawer();
  });

  // --- Open category from URL hash on load ---------------------------------
  window.addEventListener("DOMContentLoaded", () => {
    const id = (location.hash || "").replace("#", "");
    if (id && data.categories.some((c) => c.id === id)) {
      // small delay so reveal animations don't fight the modal
      setTimeout(() => openDrawer(id), 250);
    }
  });

  // --- Reveal-on-scroll -----------------------------------------------------
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("shown");
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
})();
