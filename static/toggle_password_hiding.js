document.addEventListener("DOMContentLoaded", function () {
    let toggle1 = document.getElementById("togglePassword1");
    let input1 = document.getElementById("ParolaInput");

    toggle1.addEventListener("click", function () {
        let isPassword = input1.type === "password";
        input1.type = isPassword ? "text" : "password";
        toggle1.classList.toggle("fa-eye");
        toggle1.classList.toggle("fa-eye-slash");
    });

    let toggle2 = document.getElementById("togglePassword2");
    let input2 = document.getElementById("ConfirmaParolaInput");

    toggle2.addEventListener("click", function () {
        let isPassword = input2.type === "password";
        input2.type = isPassword ? "text" : "password";
        toggle2.classList.toggle("fa-eye");
        toggle2.classList.toggle("fa-eye-slash");
    });
});
