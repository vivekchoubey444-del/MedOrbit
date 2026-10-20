(() => {
  "use strict";

  const form = document.querySelector("[data-medorbit-search]");
  if (!form) return;

  const input = form.querySelector('input[name="q"]');
  const output = document.querySelector("[data-search-results]");
  if (!input || !output) {
    console.error("MEDORBIT search: missing input or results container.");
    return;
  }

  const endpoint = form.dataset.searchEndpoint || "/api/v1/search";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = input.value.trim();
    output.replaceChildren();

    if (!query) {
      output.textContent = "Enter a search term.";
      return;
    }

    output.textContent = "Searching…";

    try {
      const url = new URL(endpoint, window.location.origin);
      url.searchParams.set("q", query);

      const response = await fetch(url, {
        headers: { Accept: "application/json" }
      });

      if (!response.ok) {
        throw new Error(`Search request failed (${response.status}).`);
      }

      const data = await response.json();

      output.replaceChildren();

      if (!Array.isArray(data.results) || data.results.length === 0) {
        output.textContent = "No matching results found.";
        return;
      }

      const list = document.createElement("ul");

      for (const result of data.results) {
        if (
          typeof result.title !== "string" ||
          typeof result.url !== "string"
        ) continue;

        const item = document.createElement("li");
        const link = document.createElement("a");

        link.textContent = result.title;
        link.href = result.url;
        item.appendChild(link);
        list.appendChild(item);
      }

      if (!list.children.length) {
        output.textContent = "No valid results returned.";
      } else {
        output.appendChild(list);
      }
    } catch (error) {
      console.error("MEDORBIT search error:", error);
      output.textContent =
        "Search is temporarily unavailable. Please try again.";
    }
  });
})();
