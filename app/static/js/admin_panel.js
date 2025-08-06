document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-parametros");
    const tabla = document.getElementById("tabla-parametros");

    const proyectoSelect = document.getElementById("proyecto_id");
    const tipoTestSelect = document.getElementById("tipo_test");
    const unidadSelect = document.getElementById("unidad");
    const ubicacion1 = document.getElementById("ubicacion_1");
    const ubicacion2Label = document.getElementById("label-ubicacion_2");
    const subEquipoLabel = document.getElementById("label-sub_equipo");
    const parametroIdInput = document.getElementById("parametro_id");

    async function cargarProyectosYTipos() {
        try {
            const [proyectosRes, testsRes] = await Promise.all([
                fetch("/proyectos/listar"),
                fetch("/tests/listar")
            ]);
            const proyectos = await proyectosRes.json();
            const tests = await testsRes.json();

            proyectoSelect.innerHTML = "<option value=''>Seleccione...</option>";
            proyectos.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.id;
                opt.textContent = p.nombre;
                proyectoSelect.appendChild(opt);
            });

            tipoTestSelect.innerHTML = "<option value=''>Seleccione...</option>";
            tests.forEach(t => {
                const opt = document.createElement("option");
                opt.value = t.nombre;
                opt.textContent = t.nombre.charAt(0).toUpperCase() + t.nombre.slice(1);
                tipoTestSelect.appendChild(opt);
            });
        } catch (error) {
            console.error("Error cargando proyectos y tipos:", error);
        }
    }

    function actualizarUnidades(test) {
        unidadSelect.innerHTML = "<option value=''>Seleccione unidad...</option>";
        if (window.UNIDADES_POR_TEST?.[test]) {
            window.UNIDADES_POR_TEST[test].forEach(u => {
                const opt = document.createElement("option");
                opt.value = u;
                opt.textContent = u;
                unidadSelect.appendChild(opt);
            });
        }
    }

    ubicacion1.addEventListener("change", () => {
        ubicacion2Label.style.display = ubicacion1.value === "COLO" ? "block" : "none";
    });

    document.getElementById("tipo_equipo").addEventListener("change", (e) => {
        const valor = e.target.value;
        subEquipoLabel.style.display = ["PDU", "MSB"].includes(valor) ? "block" : "none";
    });

    tipoTestSelect.addEventListener("change", () => {
        actualizarUnidades(tipoTestSelect.value);
        cargarParametros();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const id = parametroIdInput.value;
        const data = {
            proyecto_id: parseInt(proyectoSelect.value),
            test_id: tipoTestSelect.value,
            ubicacion_1: ubicacion1.value,
            numero_ubicacion_1: document.getElementById("numero_ubicacion_1").value,
            ubicacion_2: document.getElementById("ubicacion_2").value || null,
            numero_ubicacion_2: document.getElementById("numero_ubicacion_2").value || null,
            tipo_equipo: document.getElementById("tipo_equipo").value,
            numero_tipo_equipo: document.getElementById("numero_tipo_equipo").value,
            sub_equipo: document.getElementById("sub_equipo").value || null,
            numero_sub_equipo: document.getElementById("numero_sub_equipo").value || null,
            referencia: document.getElementById("referencia").value,
            logica: document.getElementById("logica").value,
            unidad: unidadSelect.value
        };

        try {
            const url = id ? `/parametros/${tipoTestSelect.value}/${id}/editar` : `/parametros/${tipoTestSelect.value}/crear`;
            const method = id ? "PUT" : "POST";

            const resp = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const res = await resp.json();
            if (resp.ok) {
                alert(res.mensaje || "Parámetro guardado");
                form.reset();
                parametroIdInput.value = "";
                cargarParametros();
            } else {
                alert(res.detail || "Error al guardar");
            }
        } catch (error) {
            console.error("Error guardando parámetro:", error);
        }
    });

    async function cargarParametros() {
        tabla.innerHTML = "";
        const tipo = tipoTestSelect.value;
        if (!tipo) return;

        try {
            const resp = await fetch(`/parametros/${tipo}/listar`);
            const datos = await resp.json();

            datos.forEach(p => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${p.id}</td>
                    <td>${p.proyecto_nombre || "-"}</td>
                    <td>${p.test_nombre || "-"}</td>
                    <td>${p.ubicacion_1} ${p.numero_ubicacion_1} ${p.ubicacion_2 || ""} ${p.numero_ubicacion_2 || ""}</td>
                    <td>${p.tipo_equipo} ${p.numero_tipo_equipo}</td>
                    <td>${p.sub_equipo || ""} ${p.numero_sub_equipo || ""}</td>
                    <td>${p.referencia}</td>
                    <td>${p.logica}</td>
                    <td>${p.unidad}</td>
                    <td>
                        <button class="editar" data-id="${p.id}">Editar</button>
                        <button class="eliminar" data-id="${p.id}">Eliminar</button>
                    </td>
                `;
                tabla.appendChild(tr);
            });

            document.querySelectorAll(".editar").forEach(btn => {
                btn.addEventListener("click", () => editarParametro(btn.dataset.id));
            });
            document.querySelectorAll(".eliminar").forEach(btn => {
                btn.addEventListener("click", () => eliminarParametro(btn.dataset.id));
            });
        } catch (error) {
            console.error("Error cargando parámetros:", error);
        }
    }

    async function editarParametro(id) {
        try {
            const tipo = tipoTestSelect.value;
            const resp = await fetch(`/parametros/${tipo}/listar`);
            const datos = await resp.json();
            const p = datos.find(x => x.id == id);

            if (!p) return alert("No se encontró el parámetro");

            parametroIdInput.value = p.id;
            proyectoSelect.value = p.proyecto_id;
            tipoTestSelect.value = p.test_nombre;
            actualizarUnidades(tipoTestSelect.value);
            ubicacion1.value = p.ubicacion_1;
            document.getElementById("numero_ubicacion_1").value = p.numero_ubicacion_1;
            document.getElementById("ubicacion_2").value = p.ubicacion_2 || "";
            document.getElementById("numero_ubicacion_2").value = p.numero_ubicacion_2 || "";
            document.getElementById("tipo_equipo").value = p.tipo_equipo;
            document.getElementById("numero_tipo_equipo").value = p.numero_tipo_equipo;
            document.getElementById("sub_equipo").value = p.sub_equipo || "";
            document.getElementById("numero_sub_equipo").value = p.numero_sub_equipo || "";
            document.getElementById("referencia").value = p.referencia;
            document.getElementById("logica").value = p.logica;
            unidadSelect.value = p.unidad;
        } catch (error) {
            console.error("Error editando parámetro:", error);
        }
    }

    async function eliminarParametro(id) {
        if (!confirm("¿Eliminar este parámetro?")) return;

        try {
            const tipo = tipoTestSelect.value;
            const resp = await fetch(`/parametros/${tipo}/${id}/eliminar`, { method: "DELETE" });
            if (resp.ok) {
                alert("Eliminado correctamente");
                cargarParametros();
            } else {
                alert("Error al eliminar");
            }
        } catch (error) {
            console.error("Error eliminando parámetro:", error);
        }
    }

    cargarProyectosYTipos();
});
