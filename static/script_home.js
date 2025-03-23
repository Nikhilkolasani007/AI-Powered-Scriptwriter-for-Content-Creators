document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(".fade-in");
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }, index * 500);
    });

    const buttons = document.querySelectorAll(".scale-on-hover");
    buttons.forEach(button => {
        button.addEventListener("mouseover", () => {
            button.style.transform = "scale(1.1)";
        });
        button.addEventListener("mouseleave", () => {
            button.style.transform = "scale(1)";
        });
    });
});