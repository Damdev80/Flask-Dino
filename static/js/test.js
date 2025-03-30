// Obtener elementos del DOM
const openModalBtn = document.getElementById('openModal');
const closeModalBtn = document.getElementById('closeModal');
const modal = document.getElementById('myModal');

// Función para abrir el modal
function openModal(userId) {
    document.getElementById("modal-" + userId).classList.remove("hidden");
}

function closeModal(userId) {
    document.getElementById("modal-" + userId).classList.add("hidden");
}

// Eventos
openModalBtn.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);

// Cerrar el modal si se hace clic fuera de él
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    closeModal();
  }
});

// Obtener elementos del DOM
const openModalBtn2 = document.getElementById('openModal2');
const closeModalBtn2 = document.getElementById('closeModal2');
const modal2 = document.getElementById('myModal2');

// Función para abrir el modal
function openModal2(userId2) {
    document.getElementById("modal2-" + userId2).classList.remove("hidden");
}

function closeModal2(userId2) {
    document.getElementById("modal2-" + userId2).classList.add("hidden");
}

// Eventos
openModalBtn2.addEventListener('click', openModal2);
closeModalBtn2.addEventListener('click', closeModal2);

// Cerrar el modal si se hace clic fuera de él
window.addEventListener('click', (e) => {
  if (e.target === modal2) {
    closeModal2();
  }
});



//-----------------





