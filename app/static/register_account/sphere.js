const cardInformation = document.querySelector('.card-information');
const sphere = document.querySelector('.sphere');

cardInformation.addEventListener('mousemove', (e) => {
    const cardRect = cardInformation.getBoundingClientRect();
    const mouseX = e.clientX - cardRect.left;
    const mouseY = e.clientY - cardRect.top;

    sphere.style.transform = `translate(${mouseX - 10}px, ${mouseY - 10}px)`; // Offset to center the sphere on the pointer
    sphere.style.opacity = '1'; // Show the sphere
});

cardInformation.addEventListener('mouseleave', () => {
    sphere.style.opacity = '0'; // Hide the sphere
});
