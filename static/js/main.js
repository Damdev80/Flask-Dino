const themeToggleBtn = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;

// Al cargar la página, verifica la preferencia guardada
if (localStorage.getItem('theme') === 'dark') {
  htmlElement.classList.add('dark');
}

themeToggleBtn.addEventListener('click', () => {
  if (htmlElement.classList.toggle('dark')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
});