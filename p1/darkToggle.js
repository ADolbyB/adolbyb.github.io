/**
 * Joel Brigida
 * Vanilla JS for Toggling from Light to Dark Mode
*/


// Get slider and indicator elements
const slider = document.getElementById('darkModeSlider');
const indicator = document.getElementById('sliderIndicator');

// Function to update mode based on slider value
function updateMode() {
  const isDarkMode = slider.value === '1';
  document.body.classList.toggle('darkMode', isDarkMode);
  indicator.textContent = isDarkMode ? 'Dark Mode' : 'Light Mode';
}

// Initialize mode based on current slider value
updateMode();

// Listen for slider value changes
slider.addEventListener('input', updateMode);