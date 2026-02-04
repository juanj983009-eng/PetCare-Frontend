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
        const respuesta = await fetch('https://petcare-api-fv8x.onrender.com/api/login', {
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
            // 1. Guardamos el nombre del usuario en la memoria del navegador
            // Esto sirve para mostrar "Hola Juan" en la otra página
            localStorage.setItem('usuario_actual', usuario);

            // 2. Redirigimos al Dashboard
            window.location.href = 'dashboard.html';
        } else {
            alert("Error: " + datos.mensaje);
        }

    } catch (error) {
        console.error("Error de conexión:", error);
        alert("No se pudo conectar con el servidor. ¿Está encendido?");
    }
    // Referencia al nuevo botón
    const botonRegistrar = document.getElementById('btn-registrar');

    botonRegistrar.addEventListener('click', async function () {
        const usuario = inputUsuario.value;
        const password = inputPassword.value;

        if (usuario === "" || password === "") {
            alert("⚠️ Escribe un usuario y contraseña para registrarte.");
            return;
        }

        try {
            // Llamamos a la ruta DE REGISTRO
            const respuesta = await fetch('https://petcare-api-fv8x.onrender.com/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario: usuario, password: password })
            });

            const datos = await respuesta.json();

            if (datos.exito) {
                alert("🎉 " + datos.mensaje + " ¡Ahora puedes iniciar sesión!");
            } else {
                alert("❌ " + datos.mensaje);
            }

        } catch (error) {
            console.error("Error:", error);
            alert("Error al intentar registrarse.");
        }
    });
});