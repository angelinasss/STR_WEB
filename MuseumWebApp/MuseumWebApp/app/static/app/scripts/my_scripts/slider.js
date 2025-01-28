class Slider {
    constructor({
        loop = true,
        navs = true,
        pags = true,
        auto = false,
        stopMouseHover = false,
        delay = 5
    }) {
        this.slides = document.querySelectorAll('.slide');
        this.slider = document.getElementById('slider');
        this.prevButton = document.getElementById('prev');
        this.nextButton = document.getElementById('next');
        this.pagination = document.getElementById('pagination').children;
        this.slideCounter = document.getElementById('slide-counter');
        this.adminControls = document.getElementById('admin-controls');
        this.rotationInput = document.getElementById('rotation-interval');
        this.updateButton = document.getElementById('update-interval');

        this.totalSlides = this.slides.length;
        this.currentSlide = 0;
        this.loop = loop;
        this.navs = navs;
        this.pags = pags;
        this.auto = auto;
        this.stopMouseHover = stopMouseHover;
        this.delay = delay * 1000;
        this.autoSlideInterval = null;

        this.init();
        this.enableAdminControls(); // Включение админ-панели
    }

    init() {
        this.setupNavs();
        this.setupPagination();
        this.updateSlideNumber();
        this.showSlide(this.currentSlide);

        if (this.auto) {
            this.startAutoSlide();
            if (this.stopMouseHover) {
                this.addHoverPause();
            }
        }
    }

    setupNavs() {
        if (this.navs) {
            this.prevButton.addEventListener('click', () => this.prevSlide());
            this.nextButton.addEventListener('click', () => this.nextSlide());
        } else {
            this.prevButton.style.display = 'none';
            this.nextButton.style.display = 'none';
        }
    }

    setupPagination() {
        if (this.pags) {
            for (let i = 0; i < this.pagination.length; i++) {
                this.pagination[i].addEventListener('click', () => this.showSlide(i));
            }
        } else {
            document.getElementById('pagination').style.display = 'none';
        }
    }

    nextSlide() {
        this.showSlide(this.currentSlide + 1);
    }

    prevSlide() {
        this.showSlide(this.currentSlide - 1);
    }

    showSlide(index) {
        if (index < 0) {
            this.currentSlide = this.loop ? this.totalSlides - 1 : 0;
        } else if (index >= this.totalSlides) {
            this.currentSlide = this.loop ? 0 : this.totalSlides - 1;
        } else {
            this.currentSlide = index;
        }

        this.slider.style.transform = `translateX(-${this.currentSlide * 100}%)`;
        this.updateSlideNumber();
        this.updatePagination();
    }

    updateSlideNumber() {
        this.slideCounter.textContent = `${this.currentSlide + 1}/${this.totalSlides}`;
    }

    updatePagination() {
        for (let i = 0; i < this.pagination.length; i++) {
            this.pagination[i].classList.remove('active');
        }
        this.pagination[this.currentSlide].classList.add('active');
    }

    startAutoSlide() {
        this.autoSlideInterval = setInterval(() => {
            this.nextSlide();
        }, this.delay);
    }

    stopAutoSlide() {
        clearInterval(this.autoSlideInterval);
    }

    addHoverPause() {
        this.slider.addEventListener('mouseenter', () => {
            this.stopAutoSlide();
        });
        this.slider.addEventListener('mouseleave', () => {
            this.startAutoSlide();
        });
    }

    enableAdminControls() {
        this.updateButton.addEventListener('click', () => {
            const newDelay = parseInt(this.rotationInput.value, 10);
            if (newDelay && newDelay > 0) {
                this.delay = newDelay * 1000;
                if (this.auto) {
                    this.stopAutoSlide();
                    this.startAutoSlide();
                }
            }
        });
    }
}

// Инициализация слайдера
const slider = new Slider({
    loop: true,
    navs: true,
    pags: true,
    auto: true,
    stopMouseHover: true,
    delay: 5
});
