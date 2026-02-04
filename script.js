const inputUsuario = document.getElementById('input-usuario');
const inputPassword = document.getElementById('input-password');
const botonIngresar = document.getElementById('btn-ingresar');

botonIngresar.addEventListener('click', async function () {

    const usuario = inputUsuario.value;
    const password = inputPassword.value;

    // 1. Validación básica visual (para no molestar al servidor por gusto)
    if (usuario === "" || password === "") {
        alert("Por favor completa todos los campos.");
        return;
    }

    try {
        // 2. Aquí ocurre la MAGIA: El Frontend "llama" al Backend
        // Usamos la dirección de tu servidor Python (localhost:5000)
        const respuesta = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST', // Método para enviar datos
            headers: {
                'Content-Type': 'application/json' // Le decimos: "Te estoy enviando JSON"
            },
            body: JSON.stringify({ // Empaquetamos los datos
                usuario: usuario,
                password: password
            })
        });

        // 3. Esperamos la respuesta del servidor
        const datos = await respuesta.json();

        // 4. Reaccionamos según lo que dijo Python
        if (datos.exito === true) {
            alert("✅ " + datos.mensaje);
            // Aquí podrías redirigir a otra página, ej: window.location.href = "/dashboard.html";
        } else {
            alert("Error: " + datos.mensaje);
        }

    } catch (error) {
        console.error("Error de conexión:", error);
        alert("No se pudo conectar con el servidor. ¿Está encendido?");
    }
});