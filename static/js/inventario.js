function abrirModal(
    id,
    nombre,
    categoria,
    precio,
    cantidad
) {

    document.getElementById("modalEditar").style.display = "block";

    document.getElementById("nombreEditar").value = nombre;

    document.getElementById("categoriaEditar").value = categoria;

    document.getElementById("precioEditar").value = precio;

    document.getElementById("cantidadEditar").value = cantidad;

    document.getElementById("formEditar").action =
        "/guardar-producto/" + id;
}

function cerrarModal() {

    document.getElementById("modalEditar").style.display = "none";
}