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


function aplicarFiltros() {

    let orden = document.getElementById("ordenar").value;
    let categoriaSeleccionada =
        document.getElementById("categoria").value.toLowerCase();

    let tabla = document.getElementById("tablaProductos");
    let filas = Array.from(tabla.rows).slice(1);

    // FILTRO POR CATEGORÍA

    filas.forEach(fila => {

        let categoria =
            fila.cells[2].innerText.toLowerCase();

        if (
            categoriaSeleccionada === "" ||
            categoria === categoriaSeleccionada
        ) {
            fila.style.display = "";
        }
        else {
            fila.style.display = "none";
        }
    });

    // ORDENAMIENTO

    filas.sort((a, b) => {

        let nombreA =
            a.cells[1].innerText.toLowerCase();

        let nombreB =
            b.cells[1].innerText.toLowerCase();

        let precioA =
            parseFloat(
                a.cells[3].innerText.replace("$", "")
            );

        let precioB =
            parseFloat(
                b.cells[3].innerText.replace("$", "")
            );

        switch (orden) {

            case "nombre_asc":
                return nombreA.localeCompare(nombreB);

            case "nombre_desc":
                return nombreB.localeCompare(nombreA);

            case "precio_asc":
                return precioA - precioB;

            case "precio_desc":
                return precioB - precioA;

            default:
                return 0;
        }
    });

    filas.forEach(fila => tabla.appendChild(fila));
}

document.querySelectorAll(".btn-editar").forEach(btn => {
    btn.addEventListener("click", function () {

        abrirModal(
            this.dataset.id,
            this.dataset.nombre,
            this.dataset.categoria,
            this.dataset.precio,
            this.dataset.cantidad
        );
    });
});