const statusElement = document.querySelector("#status");

fetch("/api/health")
  .then((response) => {
    if (!response.ok) throw new Error("API unavailable");
    return response.json();
  })
  .then((data) => {
    statusElement.textContent = `${data.app}: ${data.status}`;
  })
  .catch(() => {
    statusElement.textContent = "MEDORBIT frontend loaded.";
  });
