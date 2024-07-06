// Get the card element
const card = document.querySelector('.card-information');

// Function to determine grid cell and apply rotation
function getRotationAngles(e) {
    const cardRect = card.getBoundingClientRect();
    const cellWidth = cardRect.width / 5;
    const cellHeight = cardRect.height / 5;

    const relativeX = e.clientX - cardRect.left;
    const relativeY = e.clientY - cardRect.top;

    const cellX = Math.floor(relativeX / cellWidth);
    const cellY = Math.floor(relativeY / cellHeight);

    let angleX = 0;
    let angleY = 0;

    switch(cellY) {
        case 0:
            angleX = 20;
            break;
        case 1:
            angleX = 10;
            break;
        case 2:
            angleX = 0;
            break;
        case 3:
            angleX = -10;
            break;
        case 4:
            angleX = -20;
            break;
    }

    switch(cellX) {
        case 0:
            angleY = -10;
            break;
        case 1:
            angleY = -5;
            break;
        case 2:
            angleY = 0;
            break;
        case 3:
            angleY = 5;
            break;
        case 4:
            angleY = 10;
            break;
    }

    return { angleX, angleY };
}

// Function to handle mouse move
function onMouseMove(e) {
    const { angleX, angleY } = getRotationAngles(e);

    // Apply rotation transform to the card
    card.style.transform = `rotateX(${angleX}deg) rotateY(${angleY}deg)`;
}

// Event listeners
card.addEventListener('mouseenter', () => {
    document.addEventListener('mousemove', onMouseMove);
});

card.addEventListener('mouseleave', () => {
    document.removeEventListener('mousemove', onMouseMove);
    card.style.transition = 'transform 0.3s ease';
    card.style.transform = 'none';
});
