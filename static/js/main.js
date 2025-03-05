// Modo oscuro
const buttons = document.querySelectorAll(".theme-btn");

function setTheme(theme) {
  const root = document.documentElement;
  if (theme === "system") {
    theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  root.classList.remove("light", "dark");
  root.classList.add(theme);
  localStorage.setItem("theme", theme);
}

function loadTheme() {
  const savedTheme = localStorage.getItem("theme") || "system";
  setTheme(savedTheme);
}

buttons.forEach(button => {
  button.addEventListener("click", () => setTheme(button.id));
});

loadTheme();

// ----------------------------------------

//Bucador dinamico

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search");
  const juegos = document.querySelectorAll(".juego-card");

  searchInput.addEventListener("input", () => {
      const filtro = searchInput.value.toLowerCase();
      juegos.forEach(juego => {
          const nombre = juego.querySelector("h2").textContent.toLowerCase();
          juego.style.display = nombre.includes(filtro) ? "block" : "none";
      });
  });
});