// ======================================
// YAZI YAZMA ANİMASYONU
// ======================================

const texts = [
    "Web Development",
    "Python",
    "C# Programming",
    "SQL & Database",
    "Software Development"
];

let textIndex = 0;
let charIndex = 0;
let deleting = false;

const typingElement =
    document.getElementById("typing-text");


function typeEffect() {

    if (!typingElement) {
        return;
    }

    const currentText = texts[textIndex];


    if (!deleting) {

        typingElement.textContent =
            currentText.substring(
                0,
                charIndex + 1
            );

        charIndex++;


        if (charIndex === currentText.length) {

            deleting = true;

            setTimeout(typeEffect, 1400);

            return;
        }

    } else {

        typingElement.textContent =
            currentText.substring(
                0,
                charIndex - 1
            );

        charIndex--;


        if (charIndex === 0) {

            deleting = false;

            textIndex =
                (textIndex + 1) %
                texts.length;
        }

    }


    const speed =
        deleting ? 45 : 85;


    setTimeout(
        typeEffect,
        speed
    );
}


typeEffect();


// ======================================
// SCROLL REVEAL
// ======================================

const revealElements =
    document.querySelectorAll(".reveal");


const observer =
    new IntersectionObserver(

        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target
                        .classList
                        .add("active");

                }

            });

        },

        {
            threshold: 0.12
        }

    );


revealElements.forEach((element) => {

    observer.observe(element);

});


// ======================================
// MOUSE GLOW
// ======================================

const mouseGlow =
    document.getElementById("mouse-glow");


document.addEventListener(
    "mousemove",
    (event) => {

        if (!mouseGlow) {
            return;
        }

        mouseGlow.style.left =
            event.clientX + "px";

        mouseGlow.style.top =
            event.clientY + "px";

    }
);


// ======================================
// NAVBAR SCROLL EFEKTİ
// ======================================

const header =
    document.querySelector("header");


window.addEventListener(
    "scroll",
    () => {

        if (!header) {
            return;
        }

        if (window.scrollY > 50) {

            header.style.background =
                "rgba(5, 9, 20, 0.95)";

        } else {

            header.style.background =
                "rgba(5, 9, 20, 0.75)";

        }

    }
);