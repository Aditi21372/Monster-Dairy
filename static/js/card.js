function toggleCard() {
    var overlay = document.getElementById("overlay");
    var card = document.getElementById("profile-card");
    overlay.style.display = "block";
    card.style.display = "block";
  }

const noButton = document.getElementById("no");
const overlay = document.getElementById("overlay");
const card = document.getElementById("profile-card");

noButton.addEventListener("click", function() {
    overlay.style.display = "none";
    card.style.display = "none";
});

function toggleCard2() {
  var overlay = document.getElementById("overlay2");
  var card = document.getElementById("profile-card2");
  overlay.style.display = "block";
  card.style.display = "block";
}

const noButton2 = document.getElementById("no2");
const overlay2 = document.getElementById("overlay2");
const card2 = document.getElementById("profile-card2");

noButton2.addEventListener("click", function() {
  overlay2.style.display = "none";
  card2.style.display = "none";
});

const dropdown = document.querySelector('.dropdown');
const dropdownToggle = dropdown.querySelector('.dropdown-toggle');
const dropdownMenu = dropdown.querySelector('.dropdown-menu');

dropdownToggle.addEventListener('click', function() {
  dropdownMenu.classList.toggle('show');
});

dropdownMenu.addEventListener('click', function(event) {
  event.preventDefault();
  const target = event.target;
  if (target.matches('.dropdown-item')) {
    dropdownToggle.textContent = target.textContent;
    dropdownToggle.dataset.value = target.dataset.value;
  }
});
