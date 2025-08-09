function initFormContactResistance(powerType) {
    const cableSetInput = document.getElementById("cable_set");
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");

    const points = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    function generateCombination(list) {
        const combo = [];
        for (let i = 0; i < list.length; i++) {
            for (let j = i + 1; j < list.length; j++) {
                combo.push(`${list[i]}-${list[j]}`);
            }
        }
        return combo;
    }

    const combination = generateCombination(points);

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

        // Unidades
        if (window.UNIT_BY_TEST && window.UNIT_BY_TEST["contact_resistance"]) {
            const unitSelect = document.getElementById("unit");
            const labelUnit = document.getElementById("label-unit");

            if (unitSelect && labelUnit) {
                unitSelect.innerHTML = '<option value="">Select unit...</option>';
                window.UNIT_BY_TEST["contact_resistance"].forEach((u) => {
                    const opt = document.createElement("option");
                    opt.value = u;
                    opt.textContent = u;
                    unitSelect.appendChild(opt);
                });
                labelUnit.style.display = "block";
            }
        }

        const selectedUnit = document.getElementById("unit")?.value || "";
        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");

            table.innerHTML = `
                <caption>Contact Resistance - Cable Set ${i}</caption>
                <tr>
                    <th>Point</th>
                    <th>Result / N/A</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>`;

            combination.forEach((point) => {
                const row = document.createElement("tr");
                const idResult = `result_${i}_${point}`;
                const idNA = `na_${i}_${point}`;

                row.innerHTML = `
                    <td>${point}</td>
                    <td>
                        <div class="result-combined">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResult}" id="${idResult}" />
                        </div>
                    </td>
                    <td><input type="text" value="${selectedUnit}" readonly name="unit_${i}_${point}" /></td>
                    <td><input name="observation_${i}_${point}" type="text" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="attach-text"></span>
                            <input type="file" accept="image/*" name="image_${i}_${point}" style="display:none;" />
                        </label>
                    </td>
                `;
                table.appendChild(row);

                // Botón N/A
                const inputResult = row.querySelector(`#${idResult}`);
                const buttonNA = row.querySelector(`#${idNA}`);
                buttonNA.addEventListener("click", () => {
                    const isActive = !inputResult.disabled;
                    inputResult.disabled = isActive;
                    inputResult.value = isActive ? "N/A" : "";
                    buttonNA.classList.toggle("active");
                });

                // Vista previa adjunto
                const label = row.querySelector("label");
                const inputFile = label.querySelector("input[type='file']");
                const attachText = label.querySelector(".attach-text");
                inputFile.addEventListener("change", () => {
                    attachText.textContent = inputFile.files.length ? "📌 File attached" : "";
                });
            });

            resultContainer.appendChild(table);
        }
    }

    cableSetInput.addEventListener("input", generateFields);
    generateFields();

    document.getElementById("unit").addEventListener("change", () => {
        document.querySelectorAll("input[name^='unit_']").forEach(input => {
            input.value = document.getElementById("unit").value;
        });
    });

    document.getElementById("form-test").addEventListener("submit", async function (e) {
        const type = document.getElementById("test-type")?.value;
        if (type !== "contact_resistance") return;

        e.preventDefault();
        const cableSets = parseInt(cableSetInput.value);
        if (!cableSets) return alert("Enter cable set quantity.");
        if (!document.getElementById("unit").value) return alert("Select a unit before saving.");

        const results = [];
        const formData = new FormData();

        [
            "project_id", "location_1", "number_location_1",
            "location_2", "number_location_2", "equipment_type",
            "number_equipment_type", "sub_equipment", "number_sub_equipment",
            "terminal", "power_type", "test_type", "unit"
        ].forEach(field => {
            formData.append(field, document.getElementById(field)?.value || "");
        });
        formData.append("cable_set", cableSets);
        formData.append("completed", true);

        for (let i = 1; i <= cableSets; i++) {
            for (const point of combination) {
                const result = document.querySelector(`[name="result_${i}_${point}"]`)?.value || "";
                const observation = document.querySelector(`[name="observation_${i}_${point}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${point}"]`);
                const image = imageInput?.files[0];

                results.push({
                    cable_set: i,
                    test_point: point,
                    result_value: result === "N/A" ? null : parseFloat(result) || null,
                    unit: document.getElementById("unit").value,
                    observation: observation
                });

                if (image) formData.append("images", image);
            }
        }

        formData.append("data", JSON.stringify(results));

        try {
            const response = await fetch("/form/save", {
                method: "POST",
                body: formData
            });

            const res = await response.json();
            alert(response.ok ? (res.message || "✅ Contact resistance test saved successfully") : (res.detail || "❌ Error saving contact resistance test"));
        } catch (err) {
            console.error(err);
            alert("❌ Error connecting to server");
        }
    });
}

window.initFormContactResistance = initFormContactResistance;

window.loadExistingTest = function (testData) {
    document.getElementById("project_id").value = testData.project_id;
    document.getElementById("test-type").value = testData.test_type;
    document.getElementById("cable_set").value = testData.results.length
        ? Math.max(...testData.results.map(r => r.cable_set))
        : 0;

    initFormContactResistance(document.getElementById("power_type").value);

    testData.results.forEach(r => {
        const resultInput = document.querySelector(`[name="result_${r.cable_set}_${r.test_point}"]`);
        const obsInput = document.querySelector(`[name="observation_${r.cable_set}_${r.test_point}"]`);
        const unitInput = document.querySelector(`[name="unit_${r.cable_set}_${r.test_point}"]`);

        if (resultInput) resultInput.value = r.result_value || "";
        if (obsInput) obsInput.value = r.observation || "";
        if (unitInput) unitInput.value = r.unit || "";

        if (r.result_value === null) {
            resultInput.disabled = true;
            resultInput.value = "N/A";
            const naBtn = document.getElementById(`na_${r.cable_set}_${r.test_point}`);
            if (naBtn) naBtn.classList.add("active");
        }
    });
};
