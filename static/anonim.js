document.addEventListener("DOMContentLoaded", () => {
    const butonAnonim = document.getElementById("ButonAnonim");
    const butonDeconectare = document.getElementById("ButonDeconectare");

    if (butonAnonim) {
        butonAnonim.addEventListener("click", () => {
            sessionStorage.setItem("Anonim", "true");
            console.log("A fost selectată opțiunea - completare anonimă");
            window.location.href = "/meniu";
        });
    }

    const esteAnonim = sessionStorage.getItem("Anonim") === "true";

    if (esteAnonim) {
        document.querySelectorAll(".formular").forEach(el => {
            if (el.dataset.anonim !== "true") {
                el.style.display = "none";
            }
        });
    }

    if (butonDeconectare) {
        butonDeconectare.addEventListener("click", () => {
            sessionStorage.removeItem("Anonim");
            console.log("Utilizator deconectat. Anonim resetat.");
            window.location.href = "/";
        });
    }
});
