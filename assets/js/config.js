(() => {
  "use strict";
  const prefix = window.MEDORBITS?.apiPrefix || "/api/v1";
  window.MedOrbitsConfig = Object.freeze({
    getApiURL(path = "") {
      const clean = String(path).replace(/^\/+/, "");
      return prefix.replace(/\/+$/, "") + (clean ? "/" + clean : "");
    }
  });
})();
