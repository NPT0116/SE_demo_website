document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#moving-sphere');
    // const colors = ['#2e00ba', '#a60024', '#7100ff', 'purple', '#00027d'];
    const colors = ['blue', '#f7082d', '#56007b'];
    // const colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange'];
    const numSpheres = colors.length; // Number of spheres

    function createSphere(color) {
        const sphere = document.createElement('div');
        sphere.classList.add('moving-spheres');
        sphere.style.backgroundColor = color;
        container.appendChild(sphere);
        return sphere;
    }

    const spheres = colors.map(createSphere);

    const speed = 0.001; // Speed of movement
    let angle = 0;
    const scaleSpeed = 0.001; // Speed of scaling
    let scaleAngle = 0;

    function animate() {
        angle += speed;
        scaleAngle += scaleSpeed;

        spheres.forEach((sphere, index) => {
            const x = (Math.cos(angle + index) + 1) * (container.clientWidth - 100) / 2 - 100;
            const y = (Math.sin(angle + index) + 1) * (container.clientHeight - 100) / 2 - 100;
            const scale = 1 + Math.sin(scaleAngle + index) * 0.5; // Scale between 0.5 and 1.5

            sphere.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
        });

        requestAnimationFrame(animate);
    }

    animate();
});
