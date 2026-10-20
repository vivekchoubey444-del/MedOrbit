window.MedOrbitsUtils = Object.freeze({
  escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch =>
      ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[ch]);
  }
});
