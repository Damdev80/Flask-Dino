const API_KEY = '7f1803aa44754a86862da2c0715ca900';
const API_URL = `https://api.rawg.io/api/games?key=${API_KEY}`;

async function fetchGames() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const data = await response.json();
        return data.results.slice(0, 60); // Obtenemos los primeros 30 juegos
    } catch (error) {
        console.error("Error al obtener los juegos:", error);
        return [];
    }
}

const API_KEY2 ='';
const API_URL2 ='';

async function fetchNumber() {
    try {
        
    } catch (error) {
        
    }
}

function createGameCard(game) {
    const card = document.createElement('div');
    card.className = 'w-72 rounded-sm shadow-lg cursor-pointer';

    const image = document.createElement('img');
    image.src = game.background_image;
    image.alt = game.name;
    image.className = 'w-[250px] h-[380px] object-cover rounded-sm opacity-50 hover:opacity-100 transition-opacity';

    card.appendChild(image);

    // Añadir evento de clic para abrir la ventana modal
    card.addEventListener('click', () => openModal(game));

    return card;
}

async function displayGames() {
    const games = await fetchGames();
    const carousel = document.getElementById('carousel');

    // Duplicamos los juegos para el efecto de carrusel infinito
    const allGames = [...games, ...games, ...games];

    allGames.forEach(game => {
        const gameCard = createGameCard(game);
        carousel.appendChild(gameCard);
    });
}

function openModal(game) {
    const modal = document.getElementById('gameModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');

    modalImage.src = game.background_image;
    modalTitle.textContent = game.name;
    modalDescription.textContent = game.released; // Puedes cambiar esto por una descripción si está disponible

    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('gameModal');
    modal.style.display = 'none';
}

// Cerrar la ventana modal al hacer clic en la 'x'
document.querySelector('.close').addEventListener('click', closeModal);

// Cerrar la ventana modal al hacer clic fuera de ella
window.addEventListener('click', (event) => {
    const modal = document.getElementById('gameModal');
    if (event.target === modal) {
        closeModal();
    }
});

displayGames();
