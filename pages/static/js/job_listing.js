function toggleDescription(button, jobId) {
  // $(button).siblings(`#description-${jobId}`).toggle();
  var descriptionElement = document.getElementById('description-' + jobId);
    if (descriptionElement.style.display === 'none' || descriptionElement.style.display === '') {
        descriptionElement.style.display = 'block';
        descriptionElement.classList.add('active-description'); // Add class when shown
    } else {
        descriptionElement.style.display = 'none';
        descriptionElement.classList.remove('active-description'); // Remove class when hidden
    }
}
