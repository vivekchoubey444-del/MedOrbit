(() => {
  "use strict";

  const API = window.MEDORBIT_API_BASE || "";
  const $ = (selector, root = document) => root.querySelector(selector);

  function announce(element, message, state = "") {
    if (!element) return;
    element.textContent = message;
    element.dataset.state = state;
  }

  async function apiRequest(path, options = {}) {
    const response = await fetch(API + path, {
      credentials: "same-origin",
      ...options,
      headers: {
        ...(options.body instanceof FormData ? {} : {"Content-Type": "application/json"}),
        ...(options.headers || {})
      }
    });
    const type = response.headers.get("content-type") || "";
    const data = type.includes("application/json")
      ? await response.json()
      : {message: await response.text()};
    if (!response.ok) throw new Error(data.message || `Request failed (${response.status})`);
    return data;
  }

  // Connect existing search forms without replacing their current markup.
  document.querySelectorAll('form[data-mo-search], form[role="search"], form.search-form, form.search-form-inline')
    .forEach(form => {
      if (form.dataset.moBound) return;
      form.dataset.moBound = "1";
      form.addEventListener("submit", async event => {
        event.preventDefault();
        const input = form.querySelector('input[type="search"], input[name="q"], input[name="query"], input[type="text"]');
        const query = input?.value?.trim();
        if (!query) return;
        let results = form.parentElement.querySelector(".mo-results");
        if (!results) {
          results = document.createElement("div");
          results.className = "mo-results";
          results.setAttribute("aria-live", "polite");
          form.insertAdjacentElement("afterend", results);
        }
        results.textContent = "Searching MedOrbits…";
        try {
          const data = await apiRequest("/api/v1/search?q=" + encodeURIComponent(query));
          const items = Array.isArray(data.results) ? data.results : (Array.isArray(data.items) ? data.items : []);
          results.replaceChildren();
          if (!items.length) {
            results.textContent = "No matching results found.";
            return;
          }
          items.forEach(item => {
            const card = document.createElement("article");
            card.className = "mo-result";
            const title = document.createElement("div");
            title.textContent = item.title || item.name || "Search result";
            card.append(title);
            if (item.description || item.summary) {
              const description = document.createElement("p");
              description.textContent = item.description || item.summary;
              card.append(description);
            }
            if (typeof item.url === "string" && (item.url.startsWith("/") || item.url.startsWith("https://"))) {
              const link = document.createElement("a");
              link.href = item.url;
              link.textContent = "Open result";
              card.append(link);
            }
            results.append(card);
          });
        } catch (error) {
          results.textContent = "Search service is unavailable. Please try again later.";
          console.error("MedOrbits search:", error);
        }
      });
    });

  // Render optional catalog grids from the JSON data layer.
  document.querySelectorAll("[data-mo-catalog]").forEach(async grid => {
    const dataset = grid.dataset.moCatalog;
    if (!/^[a-z0-9-]+$/i.test(dataset || "")) return;
    try {
      const response = await fetch(`/assets/data/${dataset}.json`);
      if (!response.ok) throw new Error("Dataset unavailable");
      const json = await response.json();
      const items = Array.isArray(json) ? json : (json.items || []);
      grid.replaceChildren();
      items.forEach(item => {
        const article = document.createElement("article");
        article.className = "mo-card";
        const heading = document.createElement("h3");
        heading.textContent = item.title || item.name || item.courseName || "Catalog item";
        article.append(heading);
        const description = document.createElement("p");
        description.textContent = item.description || item.summary || "Explore details and available guidance.";
        article.append(description);
        if (typeof item.url === "string" && item.url.startsWith("/")) {
          const link = document.createElement("a");
          link.className = "mo-button";
          link.href = item.url;
          link.textContent = "Explore";
          article.append(link);
        }
        grid.append(article);
      });
      if (!items.length) grid.textContent = "Catalog data will appear here when the dataset is populated.";
    } catch (error) {
      console.warn(`MedOrbits catalog "${dataset}":`, error);
    }
  });

  // Account forms call the backend; no passwords or tokens are stored in the browser.
  document.querySelectorAll("[data-mo-auth]").forEach(form => {
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const status = $(".mo-status", form);
      const values = Object.fromEntries(new FormData(form).entries());
      const action = form.dataset.moAuth;
      const routes = {
        login: "/api/v1/auth/login",
        register: "/api/v1/auth/register",
        profile: "/api/v1/auth/me"
      };
      try {
        const data = await apiRequest(routes[action], {
          method: action === "profile" ? "GET" : "POST",
          ...(action === "profile" ? {} : {body: JSON.stringify(values)})
        });
        announce(status, data.message || "Request completed.", "success");
        if (action === "login" && data.user) location.href = "/auth/profile.html";
        if (action === "register" && data.user) location.href = "/auth/login.html";
      } catch (error) {
        announce(status, error.message || "The account service is not configured yet.", "error");
      }
    });
  });

  const profile = $("[data-mo-profile]");
  if (profile) {
    apiRequest("/api/v1/auth/me")
      .then(data => {
        const user = data.user || data;
        profile.textContent = "";
        ["name", "fullName", "email", "role"].forEach(key => {
          if (user[key]) {
            const row = document.createElement("p");
            row.textContent = `${key}: ${user[key]}`;
            profile.append(row);
          }
        });
      })
      .catch(() => {
        profile.textContent = "Please sign in to view your profile. The authentication API must be configured.";
      });
  }

  // Upload only to the site's conversion API; the server must validate and convert the file.
  const conversionForm = $("[data-mo-convert]");
  if (conversionForm) {
    conversionForm.addEventListener("submit", async event => {
      event.preventDefault();
      const status = $(".mo-status", conversionForm);
      const file = $('input[type="file"]', conversionForm)?.files?.[0];
      if (!file) return announce(status, "Choose a file first.", "error");
      const allowed = /\.(pdf|docx|doc|pptx|ppt|xlsx|xls|txt|html)$/i.test(file.name);
      if (!allowed) return announce(status, "This file type is not enabled in the template.", "error");
      const maxBytes = 20 * 1024 * 1024;
      if (file.size > maxBytes) return announce(status, "Maximum upload size is 20 MB.", "error");
      const body = new FormData();
      body.append("file", file);
      body.append("template", "medorbits-royal-sapphire");
      announce(status, "Uploading file for conversion…");
      try {
        const response = await fetch(API + "/api/v1/documents/convert", {
          method: "POST", credentials: "same-origin", body
        });
        if (!response.ok) {
          let message = "Conversion service is unavailable or not configured.";
          try { message = (await response.json()).message || message; } catch {}
          throw new Error(message);
        }
        const blob = await response.blob();
        const disposition = response.headers.get("content-disposition") || "";
        const match = disposition.match(/filename="?([^";]+)"?/i);
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = match ? match[1] : "MedOrbits-Document";
        document.body.append(anchor);
        anchor.click();
        anchor.remove();
        setTimeout(() => URL.revokeObjectURL(url), 30000);
        announce(status, "Converted file received. Check your downloads.", "success");
      } catch (error) {
        announce(status, error.message, "error");
      }
    });
  }
})();
