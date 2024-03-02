function toggleDescription(button, jobId) {
  $(button).siblings(`#description-${jobId}`).toggle();
}

document.addEventListener("DOMContentLoaded", function() {
  const textElement = document.getElementById("text");
  const texts = ["What do you want to do day-to-day?", 
    "Can you describe the skills or qualifications you possess?", 
    "What industry or field are you looking to work in?",
    "Are there particular challenges you enjoy tackling in your work?",
    "What technical skills are you proficient in and hope to utilize?",
    "Do you have any preferred work schedule?"]; // Your list of texts
  let index = 0;

  function changeText() {
    textElement.textContent = texts[index];
    index = (index + 1) % texts.length;
  }

  function fadeIn() {
    textElement.style.opacity = "1";
    textElement.style.transition = "opacity 0.5s ease-in-out"; // Add CSS transition
  }

  function fadeOut() {
    textElement.style.opacity = "0";
  }

  // Initial text display
  changeText(); // Display initial text
  fadeIn(); // Fade in initially

  // Start text rotation after a delay
  setTimeout(function() {
    setInterval(function() {
      fadeOut(); // Fade out
      setTimeout(function() {
        changeText(); // Change text
        fadeIn(); // Fade in
      }, 500); // Delay before fading in again
    }, 5000); // Interval for changing text (adjust as needed)
  }, 1000); // Delay before starting text rotation (adjust as needed)
});


document.addEventListener("DOMContentLoaded", function() {
  const cvLabel = document.getElementById("cvLabel");
  const cvForm = document.getElementById("cvForm");
  const cvInput = document.getElementById("id_pdf");
  const submitButton = document.getElementById("submitButton");

  cvLabel.addEventListener("click", function() {
    cvForm.style.display = "block";
    cvInput.style.display = "block";
    cvLabel.style.display = "none";
});

  // When the file input changes (i.e., the user selects a file), submit the form
  cvInput.addEventListener("change", function() {
      submitButton.click(); // Trigger a click event on the submit button
  });
});