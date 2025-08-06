// ✅ Static Units by Test Type
(function () {
    const UNIT_BY_TEST = {
        continuity: ["Ω", "mΩ", "kΩ"],
        insulation: ["MΩ", "GΩ", "kΩ"],
        contact_resistance: ["µΩ", "mΩ", "Ω"],
        torque: ["Nm", "Nmm", "kNm"],
        voltage: ["V", "mV", "kV"],
        current: ["A", "mA", "kA", "µA"],
        time: ["ms", "s", "min", "h"],
        pressure: ["bar", "psi", "kPa"] // 🔜 Ejemplo para futura expansión
    };

    if (!window.UNIT_BY_TEST) {
        window.UNIT_BY_TEST = UNIT_BY_TEST;
    } else {
        console.warn("⚠️ UNIT_BY_TEST was already defined.");
    }
})();

/**
 * ✅ Carga dinámicamente las unidades en el <select> principal
 * @param {string} testType - Tipo de test (ej: "continuity", "torque")
 */
function loadUnitByTest(testType) {
    const unitSelect = document.getElementById("unit");
    const labelUnit = document.getElementById("label-unit");

    if (!unitSelect || !labelUnit) {
        console.warn("❌ No se encontró el <select> de unidades o su etiqueta.");
        return;
    }

    // Reinicia el <select>
    unitSelect.innerHTML = '<option value="">Selecciona unidad...</option>';

    const units = window.UNIT_BY_TEST[testType] || [];
    if (units.length > 0) {
        units.forEach(u => {
            const option = document.createElement("option");
            option.value = u;
            option.textContent = u;
            unitSelect.appendChild(option);
        });
        labelUnit.style.display = "block";
    } else {
        labelUnit.style.display = "none";
    }
}

/**
 * ✅ Sincroniza automáticamente todos los campos "unit_" cuando se cambia la unidad global
 */
document.getElementById("unit")?.addEventListener("change", () => {
    const selectedUnit = document.getElementById("unit").value;

    document.querySelectorAll("#result-container input[name^='unit_']").forEach(input => {
        input.value = selectedUnit;
    });
});
