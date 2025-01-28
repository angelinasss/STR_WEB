const statues = document.querySelectorAll('.statue-container .statue');

function handleScroll() {
    const scrollY = window.scrollY;
    const windowHeight = window.innerHeight;

    statues.forEach(statue => {
        const sectionTop = statue.parentElement.parentElement.offsetTop;
        const sectionHeight = statue.parentElement.parentElement.offsetHeight;

        if (
            scrollY + windowHeight > sectionTop + sectionHeight * 0.25 &&
            scrollY < sectionTop + sectionHeight * 0.75
        ) {
            const position = statue.dataset.position;

            statue.classList.add('active');
            if (position === 'left') statue.classList.add('left-active');
            if (position === 'right') statue.classList.add('right-active');
        } else {
            statue.classList.remove('active', 'left-active', 'right-active');
        }
    });
}

window.addEventListener('scroll', handleScroll);