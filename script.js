// Comprobamos sesión al inicio
if (localStorage.getItem('logeado') !== 'true') {
    window.location.href = "login.html";
}

document.getElementById('nombre-perfil').innerText = localStorage.getItem('nombreUsuario');

function cargarCitas() {
    // Sacamos el nombre del usuario que guardamos al hacer login
    const miUsuario = localStorage.getItem('nombreUsuario');

    // Se lo pasamos a la API en la URL (?usuario=...)
    fetch(`http://172.31.1.205:5000/citas?usuario=${miUsuario}`)
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-citas');
            contenedor.innerHTML = ''; 
            
            data.forEach(c => {
                const idDiv = "desc-" + c.paciente.replace(/\s+/g, ''); 
                contenedor.innerHTML += `
                    <div class="card-cita">
                        <div onclick="toggleDescripcion('${idDiv}')" style="cursor:pointer;">
                            <div class="hora">${c.hora}</div>
                            <h3>${c.paciente}</h3>
                            <p>${c.especialidad}</p>
                        </div>
                        <div id="${idDiv}" class="desplegable">
                            <p><strong>Nota:</strong> ${c.descripcion}</p>
                        </div>
                        <button onclick="borrarCita('${c.paciente}')" class="btn-borrar">DAR DE ALTA</button>
                    </div>
                `;
            });
        });
}
function cargarCitas() {
    // Sacamos el nombre del usuario que guardamos al hacer login
    const miUsuario = localStorage.getItem('nombreUsuario');

    // Se lo pasamos a la API en la URL (?usuario=...)
    fetch(`http://172.31.1.205:5000/citas?usuario=${miUsuario}`)
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-citas');
            contenedor.innerHTML = ''; 
            
            data.forEach(c => {
                const idDiv = "desc-" + c.paciente.replace(/\s+/g, ''); 
                contenedor.innerHTML += `
                    <div class="card-cita">
                        <div onclick="toggleDescripcion('${idDiv}')" style="cursor:pointer;">
                            <div class="hora">${c.hora}</div>
                            <h3>${c.paciente}</h3>
                            <p>${c.especialidad}</p>
                        </div>
                        <div id="${idDiv}" class="desplegable">
                            <p><strong>Nota:</strong> ${c.descripcion}</p>
                        </div>
                        <button onclick="borrarCita('${c.paciente}')" class="btn-borrar">DAR DE ALTA</button>
                    </div>
                `;
            });
        });
}

function toggleDescripcion(id) {
    const el = document.getElementById(id);
    if(el) {
        el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
    }
}

function borrarCita(nombre) {
    if(confirm("¿Seguro que quieres borrar a " + nombre + "?")) {
        fetch('http://172.31.1.205/citas/' + nombre, { method: 'DELETE' })
        .then(() => {
            alert("Paciente borrado");
            cargarCitas();
        })
        .catch(err => alert("Error al borrar"));
    }
}

function cerrarSesion() {
    localStorage.clear();
    window.location.href = "login.html";
}

// Arrancar al cargar la página
document.addEventListener('DOMContentLoaded', cargarCitas);
