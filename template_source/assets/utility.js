/* Modified from https://codepen.io/jsstrn/pen/mMMmZB */

const getFontSize = (textLength, subtitle) => {
    const baseSize = 23

    if (textLength >= baseSize) {
      textLength = baseSize - 2
    }

    fontSize = 100

    if (subtitle) fontSize = baseSize/2 - textLength
    else fontSize = baseSize - textLength + 1

    return `${fontSize}vw`
}
  
window.addEventListener('load', function () {
    const title = document.querySelectorAll('.banner_txt p')
  
    title.forEach(title => {
        title.style.fontSize = getFontSize(title.textContent.length, 0)
    })

    const subtitle = document.querySelectorAll('.content_subtitle')
  
    subtitle.forEach(subtitle => {
        subtitle.style.fontSize = getFontSize(subtitle.textContent.length, 1)
    })

    /* https://blog.logrocket.com/build-image-carousel-from-scratch-vanilla-javascript/ */

    const slides = document.querySelectorAll(".content_screenshot");

    slides.forEach((slide, indx) => {
        slide.style.transform = `translateX(${indx * 100}%)`;
    });

    const nextSlide = document.querySelector(".content_gallery_btn_next");


    let curSlide = 0;
    let maxSlide = slides.length - 1;

    nextSlide.addEventListener("click", function () {
        if (curSlide === maxSlide) {
            curSlide = 0;
        } else {
            curSlide++;
        }

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
        });
    });

    const prevSlide = document.querySelector(".content_gallery_btn_prev");

    prevSlide.addEventListener("click", function () {
        if (curSlide === 0) {
            curSlide = maxSlide;
        } else {
            curSlide--;
        }

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
        });
    });
})