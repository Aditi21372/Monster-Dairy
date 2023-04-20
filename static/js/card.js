function toggleCard() {
    var overlay = document.getElementById("overlay");
    var card = document.getElementById("profile-card");
    if (card.style.display === "none") {
      overlay.style.display = "block";
      card.style.display = "block";
    } else {
      overlay.style.display = "none";
      card.style.display = "none";
    }
  }

const noButton = document.getElementById("no");
const overlay = document.getElementById("overlay");
const card = document.getElementById("profile-card");

noButton.addEventListener("click", function() {
    overlay.style.display = "none";
    card.style.display = "none";
});
