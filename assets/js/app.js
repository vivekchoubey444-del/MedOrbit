(() => {
"use strict";
const $ = id => document.getElementById(id);
const intro = $("intro");
if (intro) {
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || sessionStorage.getItem("mo-intro") === "1") intro.classList.add("done");
  else setTimeout(() => { intro.classList.add("done"); sessionStorage.setItem("mo-intro","1"); }, 1100);
  window.addEventListener("pageshow", () => intro.classList.add("done"), {once:true});
}
const menu = $("menuToggle"), nav = $("navLinks");
if (menu && nav) menu.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menu.setAttribute("aria-expanded", String(open));
  menu.textContent = open ? "×" : "☰";
});
if ($("year")) $("year").textContent = new Date().getFullYear();

const localPages = [
 ["MBBS","/education/mbbs.html","medical neet medicine"],
 ["BDS","/education/bds.html","dentistry dental"],
 ["Paramedical","/education/paramedical.html","allied health"],
 ["AYUSH","/education/ayush.html","bams bums"],
 ["Colleges","/education/colleges.html","universities"],
 ["Scholarships","/education/scholarships.html","fees funding"],
 ["Jobs","/career/jobs.html","employment vacancy"],
 ["Career guidance","/career/guidance.html","career skills"],
 ["Recruitment","/career/recruitment.html","hiring"],
 ["Resources","/pages/resources.html","pdf guides"],
 ["Login","/auth/login.html","sign in"],
 ["Register","/auth/register.html","sign up account"]
];
async function search(query, box) {
  box.replaceChildren();
  box.style.display = "block";
  const status = document.createElement("p");
  status.textContent = "Searching…";
  box.appendChild(status);
  let items = [];
  try {
    const response = await fetch("/api/v1/search?q=" + encodeURIComponent(query), {headers:{Accept:"application/json"}});
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data.results)) items = data.results;
    }
  } catch (_) {}
  if (!items.length) {
    const q = query.toLowerCase();
    items = localPages.filter(x => (x[0]+" "+x[2]).toLowerCase().includes(q))
      .map(x => ({title:x[0],url:x[1]}));
  }
  box.replaceChildren();
  if (!items.length) { box.textContent = "No matching results. Try another term."; return; }
  for (const item of items.slice(0,12)) {
    if (typeof item.title !== "string" || typeof item.url !== "string") continue;
    const link = document.createElement("a");
    link.href = item.url;
    link.textContent = item.title;
    box.appendChild(link);
  }
}
const navSearch = $("navSearch");
if (navSearch) navSearch.addEventListener("submit", e => {
  e.preventDefault();
  const value = $("searchInput").value.trim();
  if (value) location.href = "/pages/search.html?q=" + encodeURIComponent(value);
});
const mainSearch = $("mainSearch");
if (mainSearch) mainSearch.addEventListener("submit", e => {
  e.preventDefault();
  const value = $("mainSearchInput").value.trim();
  if (value) search(value, $("searchResults"));
});
})();
