document.querySelectorAll('.box').forEach(box => {
    box.addEventListener('mouseenter', () => {
        box.classList.add('hovered');
    });
    box.addEventListener('mouseleave', () => {
        box.classList.remove('hovered');
    });
});