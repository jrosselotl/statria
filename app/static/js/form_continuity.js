function initFormContinuity(powerType) {
    const cableSetInput = document.getElementById("cable_set");
    const resultContainer = document.getElementById("result-container");
    const resultBlock = document.getElementById("result-block");

    const points = powerType === "single_phase"
        ? ["L", "N", "PE"]
        : ["L1", "L2", "L3", "N", "PE"];

    const combination = [];
    for (let i = 0; i < points.length; i++) {
        for (let j = i + 1; j < points.length; j++) {
            combination.push(`${points[i]}-${points[j]}`);
        }
    }

    function generateFields() {
        const quantity = parseInt(cableSetInput.value) || 0;
        resultContainer.innerHTML = "";
        resultBlock.style.display = quantity > 0 ? "block" : "none";

        const unitSelect = document.getElementById("unit");
        const labelUnit = document.getElementById("label-unit");
        if (window.UNIT_BY_TEST["continuity"]) {
            unitSelect.innerHTML = '<option value="">Select unit...</option>';
            window.UNIT_BY_TEST["continuity"].forEach(u => {
                const opt = document.createElement("option");
                opt.value = u;
                opt.textContent = u;
                unitSelect.appendChild(opt);
            });
            labelUnit.style.display = "block";
        }

        const selectedUnit = unitSelect.value || "";
        for (let i = 1; i <= quantity; i++) {
            const table = document.createElement("table");
            table.classList.add("test-table");
            table.innerHTML = `
                <caption>Continuity - Cable Set ${i}</caption>
                <tr>
                    <th>Point</th>
                    <th>Result / N/A</th>
                    <th>Unit</th>
                    <th>Observation</th>
                    <th>Image</th>
                </tr>
            `;

            combination.forEach(point => {
                const idResult = `result_${i}_${point}`;
                const idNA = `na_${i}_${point}`;
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${point}</td>
                    <td>
                        <div class="result-combined">
                            <button type="button" class="na-btn" id="${idNA}">N/A</button>
                            <input type="text" name="${idResult}" id="${idResult}" />
                        </div>
                    </td>
                    <td><input type="text" readonly value="${selectedUnit}" name="unit_${i}_${point}" /></td>
                    <td><input type="text" name="observation_${i}_${point}" /></td>
                    <td>
                        <label class="camera-label">
                            📷 <span class="attach-text"></span>
                            <input type="file" accept="image/*" name="image_${i}_${point}" style="display:none;" />
                        </label>
                    </td>
                `;
                table.appendChild(row);

                // N/A toggle
                const input = row.querySelector(`#${idResult}`);
                const naBtn = row.querySelector(`#${idNA}`);
                naBtn.addEventListener("click", () => {
                    input.disabled = !input.disabled;
                    input.value = input.disabled ? "N/A" : "";
                    naBtn.classList.toggle("active");
                });

                const fileInput = row.querySelector("input[type='file']");
                const attachText = row.querySelector(".attach-text");
                fileInput.addEventListener("change", () => {
                    attachText.textContent = fileInput.files.length ? "📎 File attached" : "";
                });
            });

            resultContainer.appendChild(table);
        }
    }

    cableSetInput.addEventListener("input", generateFields);
    generateFields();

    document.getElementById("unit").addEventListener("change", () => {
        const val = document.getElementById("unit").value;
        document.querySelectorAll("input[name^='unit_']").forEach(input => {
            input.value = val;
        });
    });

    document.getElementById("form-test").addEventListener("submit", async function (e) {
        const type = document.getElementById("test-type").value;
        if (type !== "continuity") return;

        e.preventDefault();
        const cableSet = parseInt(cableSetInput.value);
        if (!cableSet) return alert("Enter cable set quantity");

        const formData = new FormData();
        const results = [];

        formData.append("project_id", document.getElementById("project_id").value);
        formData.append("location_1", document.getElementById("location_1").value);
        formData.append("number_location_1", document.getElementById("number_location_1").value || 0);
        formData.append("location_2", document.getElementById("location_2").value || "");
        formData.append("number_location_2", document.getElementById("number_location_2").value || 0);
        formData.append("equipment_type", document.getElementById("equipment_type").value);
        formData.append("number_equipment_type", document.getElementById("number_equipment_type").value || 0);
        formData.append("sub_equipment", document.getElementById("sub_equipment").value || "");
        formData.append("number_sub_equipment", document.getElementById("number_sub_equipment").value || 0);
        formData.append("test_type", "continuity");
        formData.append("cable_set", cableSet);
        formData.append("power_type", document.getElementById("power_type").value);
        formData.append("terminal", document.getElementById("terminal").value || "");
        formData.append("unit", document.getElementById("unit").value);
        formData.append("completed", true);

        for (let i = 1; i <= cableSet; i++) {
            for (const point of combination) {
                const result = document.querySelector(`[name="result_${i}_${point}"]`)?.value || "";
                const obs = document.querySelector(`[name="observation_${i}_${point}"]`)?.value || "";
                const imageInput = document.querySelector(`[name="image_${i}_${point}"]`);
                const image = imageInput?.files[0];

                results.push({
                    cable_set: i,
                    test_point: point,
                    result_value: result === "N/A" ? "N/A" : parseFloat(result) || null,
                    observation: obs,
                    unit: document.getElementById("unit").value || ""
                });

                if (image) {
                    formData.append("images", image);
                }
            }
        }

        formData.append("data", JSON.stringify(results));

        try {
            const res = await fetch("/form/save", {
                method: "POST",
                body: formData
            });
            const json = await res.json();
            if (res.ok) {
                alert(json.message || "✅ Test saved successfully");
            } else {
                alert(json.detail || "❌ Error saving test");
            }
        } catch (err) {
            console.error("❌ Server error:", err);
            alert("❌ Connection error");
        }
    });
}

window.initFormContinuity = initFormContinuity;

window.loadExistingTest = function (testData) {
    document.getElementById("project_id").value = testData.project_id;
    document.getElementById("test-type").value = testData.test_type;
    document.getElementById("cable_set").value = testData.results.length
        ? Math.max(...testData.results.map(r => r.cable_set))
        : 0;

    initFormContinuity(document.getElementById("power_type").value);

    testData.results.forEach(r => {
        const resultInput = document.querySelector(`[name="result_${r.cable_set}_${r.test_point}"]`);
        const obsInput = document.querySelector(`[name="observation_${r.cable_set}_${r.test_point}"]`);
        const unitInput = document.querySelector(`[name="unit_${r.cable_set}_${r.test_point}"]`);

        if (resultInput) resultInput.value = r.result_value ?? "";
        if (obsInput) obsInput.value = r.observation ?? "";
        if (unitInput) unitInput.value = r.unit ?? "";

        if (r.result_value === null || r.result_value === "N/A") {
            resultInput.disabled = true;
            resultInput.value = "N/A";
            const naBtn = document.getElementById(`na_${r.cable_set}_${r.test_point}`);
            if (naBtn) naBtn.classList.add("active");
        }
    });
};
