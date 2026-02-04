// 1. Referenciamos los elementos del DOM (del HTML)
// Usamos 'const' porque estas referencias no van a cambiar
const inputUsuario = document.getElementById('input-usuario');
const inputPassword = document.getElementById('input-password');
const botonIngresar = document.getElementById('btn-ingresar');

// 2. Agregamos el "Oído" (Event Listener)
// Le decimos al botón: "Estate atento cuando te hagan click"
botonIngresar.addEventListener('click', function () {

    // 3. Obtenemos los valores actuales que escribió el usuario
    const usuario = inputUsuario.value;
    const password = inputPassword.value;

    // 4. Lógica de validación (El IF)
    if (usuario === "" || password === "") {
        // Si alguno está vacío...
        alert("⚠️ Error: Por favor completa todos los campos.");
    } else {
        // Si todo está lleno...
        alert("✅ ¡Bienvenido, " + usuario + "! Iniciando sistema...");
    }

});