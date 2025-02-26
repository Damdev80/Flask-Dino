//Busqueda dinamica de jeugos.
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