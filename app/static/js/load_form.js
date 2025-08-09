document.addEventListener("DOMContentLoaded", () => {
  // ------- DOM refs -------
  const projectSelect = document.getElementById("project_id");

  const location1Select = document.getElementById("location_1");
  const numberLocation1Select = document.getElementById("number_location_1");
  const location2Container = document.getElementById("label-location_2");
  const location2Select = document.getElementById("location_2");
  const numberLocation2Select = document.getElementById("number_location_2");

  const equipmentTypeSelect = document.getElementById("equipment_type");
  const numberEquipmentTypeSelect = document.getElementById("number_equipment_type");
  const subEquipmentContainer = document.getElementById("label-sub_equipment");
  const subEquipmentSelect = document.getElementById("sub_equipment");
  const numberSubEquipmentSelect = document.getElementById("number_sub_equipment");

  const specialtySelect = document.getElementById("specialty");
  const testTypeSelect = document.getElementById("test-type");

  const featureBlock = document.getElementById("block-features");
  const resultBlock = document.getElementById("result-block");
  const powerTypeSelect = document.getElementById("power_type");

  // hidden para enviar el ID real del test al backend
  let hiddenTestTypeId = document.getElementById("test_type_id");
  if (!hiddenTestTypeId) {
    hiddenTestTypeId = document.createElement("input");
    hiddenTestTypeId.type = "hidden";
    hiddenTestTypeId.id = "test_type_id";
    hiddenTestTypeId.name = "test_type_id";
    document.getElementById("form-test").appendChild(hiddenTestTypeId);
  }

  // ------- helpers -------
  const toSnake = (s) => (s || "").toLowerCase().replace(/\s+/g, "_");

  function toggleSelectVisibility(select, show) {
    if (show) {
      select.style.display = "inline-block";
      select.required = true;
    } else {
      select.style.display = "none";
      select.required = false;
      select.innerHTML = "";
    }
  }

  function resetInitialState() {
    // locations
    toggleSelectVisibility(numberLocation1Select, false);
    location2Container.style.display = "none";
    toggleSelectVisibility(numberLocation2Select, false);

    // equipment
    toggleSelectVisibility(numberEquipmentTypeSelect, false);
    subEquipmentContainer.style.display = "none";
    toggleSelectVisibility(numberSubEquipmentSelect, false);

    // specialty/test
    if (specialtySelect) {
      specialtySelect.innerHTML = "<option value=''>Select specialty...</option>";
      specialtySelect.disabled = true;
    }
    testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
    testTypeSelect.disabled = true;
    hiddenTestTypeId.value = "";
  }

  // ------- LOAD: Projects -------
  async function loadProjects() {
    try {
      const res = await fetch("/project/");
      const projects = await res.json();

      projectSelect.innerHTML = "<option value=''>Select project...</option>";
      projects.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = p.name;
        projectSelect.appendChild(opt);
      });

      projectSelect.onchange = () => {
        resetInitialState();
        if (projectSelect.value) {
          loadLocation(projectSelect.value);
          loadEquipment();
          loadSpecialtiesByProject(projectSelect.value); // specialties filtradas por proyecto
        }
      };

      // si ya viene con valor (modo edición)
      if (projectSelect.value) projectSelect.dispatchEvent(new Event("change"));
    } catch (err) {
      console.error("❌ Error loading projects:", err);
    }
  }

  // ------- LOAD: Specialties by project -------
  async function loadSpecialtiesByProject(projectId) {
    try {
      const res = await fetch(`/specialty/by_project/${projectId}`);
      const specialties = await res.json();

      specialtySelect.innerHTML = "<option value=''>Select specialty...</option>";
      specialties.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s.id;           // ID real
        opt.textContent = s.name;
        specialtySelect.appendChild(opt);
      });

      specialtySelect.disabled = specialties.length === 0;

      specialtySelect.onchange = () => {
        testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
        testTypeSelect.disabled = true;
        hiddenTestTypeId.value = "";

        const specId = parseInt(specialtySelect.value || "0", 10);
        if (specId > 0) {
          loadTestTypesByProjectAndSpecialty(projectId, specId);
        }
      };
    } catch (e) {
      console.error("❌ Error loading specialties by project:", e);
      specialtySelect.innerHTML = "<option value=''>Select specialty...</option>";
      specialtySelect.disabled = true;
    }
  }

  // ------- LOAD: Test types by project + specialty -------
  async function loadTestTypesByProjectAndSpecialty(projectId, specialtyId) {
    try {
      const url = `/test_type/by_project?project_id=${projectId}&specialty_id=${specialtyId}`;
      const testTypes = await (await fetch(url)).json(); // [{id,name,specialty_id}]

      testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
      testTypes.forEach(t => {
        const opt = document.createElement("option");
        opt.value = toSnake(t.name);  // lo usa el JS del formulario (initForm*)
        opt.textContent = t.name;     // etiqueta visible
        opt.dataset.id = t.id;        // ID real para guardar
        testTypeSelect.appendChild(opt);
      });
      testTypeSelect.disabled = testTypes.length === 0;
    } catch (err) {
      console.error("❌ Error loading test types:", err);
      testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
      testTypeSelect.disabled = true;
    }
  }

  // ------- LOAD: Locations -------
  async function loadLocation(projectId) {
    try {
      const res = await fetch(`/location/list?project_id=${projectId}`);
      const locationData = await res.json();

      location1Select.innerHTML = "<option value=''>Select</option>";
      locationData.forEach((l) => {
        const opt = document.createElement("option");
        opt.value = l.location_1;
        opt.textContent = l.location_1;
        opt.dataset.number = JSON.stringify(l.number_location_1 || []);
        opt.dataset.location2 = l.location_2 || "";
        opt.dataset.number2 = JSON.stringify(l.number_location_2 || []);
        location1Select.appendChild(opt);
      });

      location1Select.onchange = () => {
        const selected = location1Select.selectedOptions[0];
        if (!selected) return;

        const numbers1 = JSON.parse(selected.dataset.number || "[]");
        const location2 = selected.dataset.location2;
        const numbers2 = JSON.parse(selected.dataset.number2 || "[]");

        if (numbers1.length > 0) {
          toggleSelectVisibility(numberLocation1Select, true);
          numberLocation1Select.innerHTML = "";
          numbers1.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numberLocation1Select.appendChild(opt);
          });
        } else {
          toggleSelectVisibility(numberLocation1Select, false);
        }

        if (location2) {
          location2Container.style.display = "block";
          location2Select.innerHTML = `<option value="${location2}">${location2}</option>`;
          if (numbers2.length > 0) {
            toggleSelectVisibility(numberLocation2Select, true);
            numberLocation2Select.innerHTML = "";
            numbers2.forEach((n) => {
              const opt = document.createElement("option");
              opt.value = n;
              opt.textContent = n;
              numberLocation2Select.appendChild(opt);
            });
          } else {
            toggleSelectVisibility(numberLocation2Select, false);
          }
        } else {
          location2Container.style.display = "none";
          toggleSelectVisibility(numberLocation2Select, false);
        }
      };
    } catch (error) {
      console.error("❌ Error loading location:", error);
    }
  }

  // ------- LOAD: Equipment types -------
  async function loadEquipment() {
    try {
      const res = await fetch(`/equipment_type/list`);
      const equipmentData = await res.json();

      equipmentTypeSelect.innerHTML = "<option value=''>Select</option>";
      equipmentData.forEach((e) => {
        const opt = document.createElement("option");
        opt.value = e.equipment_type;
        opt.textContent = e.equipment_type;
        opt.dataset.number = JSON.stringify(e.number_equipment_type || []);
        opt.dataset.sub = e.sub_equipment || "";
        opt.dataset.numberSub = JSON.stringify(e.number_sub_equipment || []);
        equipmentTypeSelect.appendChild(opt);
      });

      equipmentTypeSelect.onchange = () => {
        const selected = equipmentTypeSelect.selectedOptions[0];
        if (!selected) return;

        const numbers = JSON.parse(selected.dataset.number || "[]");
        if (numbers.length > 0) {
          toggleSelectVisibility(numberEquipmentTypeSelect, true);
          numberEquipmentTypeSelect.innerHTML = "";
          numbers.forEach((n) => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            numberEquipmentTypeSelect.appendChild(opt);
          });
        } else {
          toggleSelectVisibility(numberEquipmentTypeSelect, false);
        }

        const sub = selected.dataset.sub;
        if (sub) {
          subEquipmentContainer.style.display = "block";
          subEquipmentSelect.innerHTML = `<option value="${sub}">${sub}</option>`;
          const numbersSub = JSON.parse(selected.dataset.numberSub || "[]");
          if (numbersSub.length > 0) {
            toggleSelectVisibility(numberSubEquipmentSelect, true);
            numberSubEquipmentSelect.innerHTML = "";
            numbersSub.forEach((n) => {
              const opt = document.createElement("option");
              opt.value = n;
              opt.textContent = n;
              numberSubEquipmentSelect.appendChild(opt);
            });
          } else {
            toggleSelectVisibility(numberSubEquipmentSelect, false);
          }
        } else {
          subEquipmentContainer.style.display = "none";
          toggleSelectVisibility(numberSubEquipmentSelect, false);
        }
      };
    } catch (error) {
      console.error("❌ Error loading equipment:", error);
    }
  }

  // ------- Change Test Type -> init forms -------
  testTypeSelect.onchange = () => {
    const type = testTypeSelect.value; // "continuity" | "insulation" | "contact_resistance" | "torque"
    const opt = testTypeSelect.selectedOptions[0];
    hiddenTestTypeId.value = opt ? (opt.dataset.id || "") : "";

    featureBlock.style.display = type ? "block" : "none";
    resultBlock.style.display = "none";

    if (type) {
      loadUnitByTest(type);
    }

    if (type === "continuity") initFormContinuity(powerTypeSelect.value);
    if (type === "insulation") initFormInsulation(powerTypeSelect.value);
    if (type === "contact_resistance") initFormContactResistance(powerTypeSelect.value);
    if (type === "torque") initFormTorque(powerTypeSelect.value);

    applyResponsiveLabels();
  };

  powerTypeSelect.onchange = () => {
    testTypeSelect.dispatchEvent(new Event("change"));
  };

  // init
  resetInitialState();
  loadProjects();
});

// -------- mobile labels --------
function applyResponsiveLabels() {
  if (window.innerWidth > 768) return;
  document.querySelectorAll(".test-table").forEach(table => {
    const headers = Array.from(table.querySelectorAll("th")).map(th => th.innerText.trim());
    table.querySelectorAll("tr").forEach(row => {
      row.querySelectorAll("td").forEach((td, index) => {
        if (headers[index]) {
          td.setAttribute("data-label", headers[index]);
        }
      });
    });
  });
}
