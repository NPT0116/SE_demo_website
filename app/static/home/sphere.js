document.addEventListener('DOMContentLoaded', () => {
    const sphereContainer = document.getElementById('sphere-container');
    const sphere = document.createElement('div');
    sphere.id = 'sphere';
    sphereContainer.appendChild(sphere);

    document.addEventListener('mousemove', (event) => {
        const x = event.clientX - sphere.offsetWidth / 2;
        const y = event.clientY - sphere.offsetHeight / 2;
        sphere.style.transform = `translate(${x}px, ${y}px)`;
    });
});
