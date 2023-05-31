//toggle functionality for light/dark modes
const sunIcon = document.getElementById("sun");
const moonIcon = document.getElementById("moon");

const userTheme = localStorage.getItem("theme");
const systemTheme = window.matchMedia("(prefered-color-scheme: dark)").matches;

const iconToggle = ()=>{
    sunIcon.classList.toggle("tw-hidden");
    moonIcon.classList.toggle("tw-hidden");
};

const themeCheck = ()=>{
    if(userTheme === "dark" || (!userTheme && systemTheme)){
        document.documentElement.classList.add("tw-dark");
        moonIcon.classList.add("tw-hidden");
        return;
    }
    sunIcon.classList.add("tw-hidden");
};

const themeSwitch = ()=> {
    if (document.documentElement.classList.contains("tw-dark")){
        document.documentElement.classList.remove("tw-dark");
        localStorage.setItem("theme", "Light");
        iconToggle();
        return;
    }
    document.documentElement.classList.add("tw-dark");
    localStorage.setItem("theme", "dark");
    iconToggle();
};

sunIcon.addEventListener("click", ()=>{
    themeSwitch();
});

moonIcon.addEventListener("click", ()=>{
    themeSwitch();
});

themeCheck();