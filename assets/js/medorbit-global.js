(() => {
  "use strict";
  document.documentElement.classList.add("medorbit-design-ready");
  document.querySelectorAll("a[href]").forEach(link => {
    const href = link.getAttribute("href");
    if (href && href.startsWith("#") && href.length > 1) {
      link.addEventListener("click", () => {
        const target = document.getElementById(href.slice(1));
        if (target) target.scrollIntoView({behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"});
      }, {passive:true});
    }
  });
})();
