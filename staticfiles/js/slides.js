let currentSlideIndex = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove('active');
    if (i === index) {
      slide.classList.add('active');
    }
  });
}

function nextSlide() {
  currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
  showSlide(currentSlideIndex);
}

function prevSlide() {
  currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
  showSlide(currentSlideIndex);
}

// Auto-slide every 5 seconds
setInterval(nextSlide, 5000);

// Initial slide
showSlide(currentSlideIndex);

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('img').forEach(function(img) {
    img.addEventListener('contextmenu', function(event) {
      event.preventDefault(); // Disable right-click
    });
  });
});
