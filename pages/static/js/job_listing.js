function toggleDescription(button, jobId) {
  $(button).siblings(`#description-${jobId}`).toggle();
}

// function toggleJobListings(button) {
//   var jobListings = button.nextElementSibling;
//   jobListings.style.display = jobListings.style.display === "none" ? "block" : "none";
// }

function toggleJobListings(titleSlug) {
  // First, hide all job listings
  document.querySelectorAll('.main-content .job-listings').forEach(function(list) {
      list.style.display = 'none';
  });

  // Then, show the one that corresponds to the clicked title
  var jobListings = document.getElementById(titleSlug);
  if (jobListings) {
      jobListings.style.display = 'block';
  }
}

function toggleJobListingsAll() {
  document.querySelectorAll('.main-content .job-listings').forEach(function(list) {
    list.style.display = 'none';
  });

    document.querySelectorAll('.main-content .job-listings').forEach(function(list) {
    list.style.display = 'block';
  });
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
  const idPdf = document.getElementById("id_pdf");

  cvLabel.addEventListener("click", function() {
      idPdf.style.display = "block";
      cvLabel.style.display = "none";
  });

  // Prevent the main form from being submitted when the CV upload form is submitted
  cvForm.addEventListener("submit", function(event) {
      event.preventDefault();
      // Your CV upload logic here...
      // Once the CV is uploaded, you can optionally show a success message
      alert("CV uploaded successfully!");
  });
});


let popup = document.getElementById('popup')

function openPopup(){
  popup.classList.add('open-popup')
}

function closePopup(){
  popup.classList.remove('open-popup')
}
