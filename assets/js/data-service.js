(() => {
  "use strict";

  const cache = new Map();

  async function load(name) {
    if (!/^[a-z0-9-]+$/.test(name)) {
      throw new Error("Invalid dataset name");
    }

    if (cache.has(name)) return cache.get(name);

    const request = fetch(`/assets/data/${name}.json`, {
      headers: { Accept: "application/json" }
    }).then(async (response) => {
      if (!response.ok) {
        throw new Error(`Dataset ${name} returned HTTP ${response.status}`);
      }
      return response.json();
    });

    cache.set(name, request);

    try {
      return await request;
    } catch (error) {
      cache.delete(name);
      throw error;
    }
  }

  function renderList(container, items, fields) {
    container.replaceChildren();

    if (!Array.isArray(items) || items.length === 0) {
      container.textContent = "Information will be published after verification.";
      return;
    }

    const list = document.createElement("ul");

    for (const item of items) {
      const li = document.createElement("li");
      const title = item.title || item.name || item.question || item.label || "Item";
      const heading = document.createElement("strong");
      heading.textContent = String(title);
      li.appendChild(heading);

      for (const field of fields) {
        if (field === "title" || field === "name") continue;
        const value = item[field];
        if (value === undefined || value === null || value === "") continue;
        const p = document.createElement("p");
        p.textContent = `${field}: ${String(value)}`;
        li.appendChild(p);
      }

      list.appendChild(li);
    }

    container.appendChild(list);
  }

  async function connect(root = document) {
    const elements = root.querySelectorAll("[data-data-source]");

    for (const element of elements) {
      const dataset = element.dataset.dataSource;
      const fields = (element.dataset.fields || "description")
        .split(",").map((field) => field.trim()).filter(Boolean);

      try {
        const data = await load(dataset);
        renderList(element, data.items, fields);
      } catch (error) {
        console.error("MEDORBIT data connection failed:", error);
        element.textContent = "Information is temporarily unavailable.";
      }
    }
  }

  window.MEDORBIT_DATA = Object.freeze({ load, connect });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => connect());
  } else {
    connect();
  }
})();
