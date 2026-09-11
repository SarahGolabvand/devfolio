const root = document.documentElement;
const themeButtons = document.querySelectorAll("[data-theme-toggle]");
const mobileMenuButton = document.querySelector("[data-menu-toggle]");
const mobileMenu = document.querySelector("[data-mobile-menu]");
const orderDialog = document.querySelector("#order-dialog");
const orderForm = document.querySelector("#order-form");
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
const projectSearch = document.querySelector("[data-project-search]");
const projectFilters = document.querySelectorAll("[data-project-filter]");
const projectCards = document.querySelectorAll("[data-project-card]");
const projectCount = document.querySelector("[data-project-count]");
const projectsEmptyState = document.querySelector("[data-projects-empty]");

const readStoredTheme = () => {
  try {
    return localStorage.getItem("theme");
  } catch {
    return null;
  }
};

const storeTheme = (theme) => {
  try {
    localStorage.setItem("theme", theme);
  } catch {}
};

const getPreferredTheme = () => {
  const storedTheme = readStoredTheme();

  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return systemTheme.matches ? "dark" : "light";
};

const updateThemeControls = (theme) => {
  themeButtons.forEach((button) => {
    const isDark = theme === "dark";
    button.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} mode`);
    button.setAttribute("title", `Switch to ${isDark ? "light" : "dark"} mode`);
    button.setAttribute("aria-pressed", String(isDark));
  });
};

const applyTheme = (theme) => {
  root.classList.toggle("dark", theme === "dark");
  root.style.colorScheme = theme;
  updateThemeControls(theme);
};

applyTheme(getPreferredTheme());

themeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const nextTheme = root.classList.contains("dark") ? "light" : "dark";
    storeTheme(nextTheme);
    applyTheme(nextTheme);
  });
});

systemTheme.addEventListener("change", (event) => {
  if (!readStoredTheme()) {
    applyTheme(event.matches ? "dark" : "light");
  }
});

if (mobileMenuButton && mobileMenu) {
  mobileMenuButton.addEventListener("click", () => {
    const isOpen = mobileMenuButton.getAttribute("aria-expanded") === "true";
    mobileMenuButton.setAttribute("aria-expanded", String(!isOpen));
    mobileMenu.classList.toggle("hidden", isOpen);
  });

  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileMenuButton.setAttribute("aria-expanded", "false");
      mobileMenu.classList.add("hidden");
    });
  });
}

document.querySelectorAll("[data-open-order]").forEach((button) => {
  button.addEventListener("click", () => {
    if (orderDialog?.showModal) {
      orderDialog.showModal();
      document.body.classList.add("overflow-hidden");
    } else {
      document.querySelector("#contact")?.scrollIntoView({ behavior: "smooth" });
    }
  });
});

document.querySelectorAll("[data-close-order]").forEach((button) => {
  button.addEventListener("click", () => orderDialog?.close());
});

orderDialog?.addEventListener("click", (event) => {
  if (event.target === orderDialog) {
    orderDialog.close();
  }
});

orderDialog?.addEventListener("close", () => {
  document.body.classList.remove("overflow-hidden");
});

orderForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const submitButton = orderForm.querySelector('button[type="submit"]');
  const originalLabel = submitButton.textContent;

  submitButton.textContent = "Inquiry sent";
  submitButton.disabled = true;

  window.setTimeout(() => {
    orderForm.reset();
    orderDialog?.close();
    submitButton.textContent = originalLabel;
    submitButton.disabled = false;
  }, 900);
});
if (projectCards.length) {
  let activeFilter = "all";

  const filterProjects = () => {
    const query = projectSearch?.value.trim().toLowerCase() ?? "";
    let visibleCount = 0;

    projectCards.forEach((card) => {
      // نرمال‌سازی تگ‌ها به حروف کوچک و حذف فاصله‌ها
      const rawCategories = card.dataset.categories ?? "";
      const categories = rawCategories
        .toLowerCase()
        .split(" ")
        .map((t) => t.trim())
        .filter((t) => t !== "");

      const searchableText = card.textContent.toLowerCase();
      const targetFilter = (activeFilter || "all").toLowerCase().trim();

      const matchesFilter =
        targetFilter === "all" || categories.includes(targetFilter);

      const matchesSearch = !query || searchableText.includes(query);
      const isVisible = matchesFilter && matchesSearch;

      card.classList.toggle("hidden", !isVisible);
      visibleCount += Number(isVisible);
    });

    if (projectCount) {
      projectCount.textContent = String(visibleCount);
    }

    projectsEmptyState?.classList.toggle("hidden", visibleCount !== 0);
  };

  projectFilters.forEach((button) => {
    button.addEventListener("click", () => {
      // دریافت فیلتر و فال‌بک به all در صورت نبود مقدار
      activeFilter = button.dataset.projectFilter || "all";

      projectFilters.forEach((filterButton) => {
        const isActive = filterButton === button;
        filterButton.setAttribute("aria-pressed", String(isActive));
        filterButton.classList.toggle("!bg-slate-950", isActive);
        filterButton.classList.toggle("!text-white", isActive);
        filterButton.classList.toggle("dark:!bg-white", isActive);
        filterButton.classList.toggle("dark:!text-slate-950", isActive);
      });

      filterProjects();
    });
  });

  projectSearch?.addEventListener("input", filterProjects);
  filterProjects();
}
