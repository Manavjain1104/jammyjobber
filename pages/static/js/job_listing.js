function toggleDescription(button, jobId) {
    var descriptionElement = document.getElementById('description-' + jobId);
      if (descriptionElement.style.display === 'none' || descriptionElement.style.display === '') {
          descriptionElement.style.display = 'block';
          descriptionElement.classList.add('active-description'); 
      } else {
          descriptionElement.style.display = 'none';
          descriptionElement.classList.remove('active-description');
      }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
      const strings = ['What do you want your job to involve?', 'Where do you want to work?', 'What skills do you have?'];
      let currentIndex = 0; 
  
      function updateText() {
          document.getElementById('rotating-question').textContent = strings[currentIndex];
          currentIndex = (currentIndex + 1) % strings.length;
      }
  
      setInterval(updateText, 4000);
  });
  