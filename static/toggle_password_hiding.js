document.addEventListener("DOMContentLoaded", function () {
    const toggle1 = document.getElementById("togglePassword1");
    const input1 = document.getElementById("ParolaInput");

    toggle1.addEventListener("click", function () {
        const isPassword = input1.type === "password";
        input1.type = isPassword ? "text" : "password";
        toggle1.classList.toggle("fa-eye");
        toggle1.classList.toggle("fa-eye-slash");
    });

    const toggle2 = document.getElementById("togglePassword2");
    const input2 = document.getElementById("ConfirmaParolaInput");

    toggle2.addEventListener("click", function () {
        const isPassword = input2.type === "password";
        input2.type = isPassword ? "text" : "password";
        toggle2.classList.toggle("fa-eye");
        toggle2.classList.toggle("fa-eye-slash");
    });
});
