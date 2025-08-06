document.addEventListener("DOMContentLoaded", () => {
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

  const testTypeSelect = document.getElementById("test-type");
  const featureBlock = document.getElementById("block-features");
  const resultBlock = document.getElementById("result-block");
  const powerTypeSelect = document.getElementById("power_type");

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
    toggleSelectVisibility(numberLocation1Select, false);
    location2Container.style.display = "none";
    toggleSelectVisibility(numberLocation2Select, false);
    toggleSelectVisibility(numberEquipmentTypeSelect, false);
    subEquipmentContainer.style.display = "none";
    toggleSelectVisibility(numberSubEquipmentSelect, false);
  }

  async function loadProjectAndTestType() {
    try {
      const [projectRes, testRes] = await Promise.all([
        fetch("/project/list"),
        fetch("/test/list")
      ]);

      const projectData = await projectRes.json();
      const testData = await testRes.json();

      const projectSelect = document.getElementById("project_id");
      projectSelect.innerHTML = "<option value=''>Select...</option>";
      projectData.forEach((p) => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = p.name;
        projectSelect.appendChild(opt);
      });

      testTypeSelect.innerHTML = "<option value=''>Select test...</option>";
      testData.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.test_type;
        opt.textContent = t.test_type.charAt(0).toUpperCase() + t.test_type.slice(1);
        testTypeSelect.appendChild(opt);
      });

      projectSelect.onchange = () => {
        resetInitialState();
        if (projectSelect.value) {
          loadLocation(projectSelect.value);
          loadEquipment();
        }
      };
    } catch (error) {
      console.error("❌ Error loading project or test type:", error);
    }
  }

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

  // ✅ Cambio de tipo de test
  testTypeSelect.onchange = () => {
    const type = testTypeSelect.value;
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

  resetInitialState();
  loadProjectAndTestType();
});

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
