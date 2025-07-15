document.addEventListener("DOMContentLoaded", () => {
    const butonAnonim = document.getElementById("ButonAnonim");

    if (butonAnonim) {
        butonAnonim.addEventListener("click", () => {
            sessionStorage.setItem("Anonim", "true");
            console.log("A fost selectată opțiunea - completare anonimă");
            window.location.href = "/meniu"; 
        });
    }

    const esteAnonim = sessionStorage.getItem("Anonim") === "true";

    if (esteAnonim) {
        const formulare = document.querySelectorAll(".formular");

        formulare.forEach(formular => {
            const anonimPermis = formular.dataset.anonim === "true";
            if (!anonimPermis) {
                formular.style.display = "none";
            }
        });
    }

    const butonDeconectare = document.getElementById("ButonDeconectare");

    if (butonDeconectare) {
        butonDeconectare.addEventListener("click", () => {
            sessionStorage.removeItem("Anonim");
            console.log("Utilizator deconectat. Anonim resetat.");
            window.location.href = "/"; 
        });
    }
});
