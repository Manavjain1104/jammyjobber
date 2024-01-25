function toggleDescription(button, jobId) {
  $(button).siblings(`#description-${jobId}`).toggle();
}