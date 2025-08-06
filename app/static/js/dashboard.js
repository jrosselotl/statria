document.addEventListener("DOMContentLoaded", () => {
  const btnDashboard = document.getElementById("btnDashboard");
  const btnMyTest = document.getElementById("btnMyTest");
  const btnNewTest = document.getElementById("btnNewTest");

  const sectionDashboard = document.getElementById("section-dashboard");
  const sectionMyTest = document.getElementById("section-mytest");
  const sectionNewTest = document.getElementById("section-newtest");

  const tableMyTest = document.getElementById("table-mytest");
  const chartCanvas = document.getElementById("chart-test");
  const userId = document.body.dataset.userId || "1"; // 🔁 Puedes reemplazar por user real

  let chartInstance = null;

  const sidebar = document.getElementById("sidebar");
  const hamburger = document.getElementById("hamburger");

  // ✅ Mostrar una sección
  function showSection(section) {
    [sectionDashboard, sectionMyTest, sectionNewTest].forEach((s) => s.classList.add("hidden"));
    section.classList.remove("hidden");
  }

  // ✅ Cargar gráfico
  async function loadChart() {
    if (!chartCanvas) return;
    try {
      const res = await fetch(`/test_run/list_user/${userId}`);
      const tests = await res.json();

      const stats = {};
      tests.forEach((t) => {
        const type = t.test_type || t.name;
        stats[type] = (stats[type] || 0) + 1;
      });

      const types = Object.keys(stats);
      const quantities = Object.values(stats);

      if (chartInstance) chartInstance.destroy();

      chartInstance = new Chart(chartCanvas, {
        type: "bar",
        data: {
          labels: types.map((t) => t.charAt(0).toUpperCase() + t.slice(1)),
          datasets: [
            {
              label: "Completed Tests",
              data: quantities,
              backgroundColor: [
                "rgba(52, 152, 219, 0.8)",
                "rgba(155, 89, 182, 0.8)",
                "rgba(230, 126, 34, 0.8)",
                "rgba(39, 174, 96, 0.8)"
              ],
              borderRadius: 8
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `Total: ${context.raw}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1, color: "#2c3e50" }
            },
            x: { ticks: { color: "#2c3e50" } }
          }
        }
      });
    } catch (err) {
      console.error("❌ Error loading chart:", err);
    }
  }

  // ✅ Cargar tabla de tests
  async function loadMyTest() {
    tableMyTest.innerHTML = "";
    try {
      const res = await fetch(`/test_run/list_user/${userId}`);
      const tests = await res.json();

      tests.forEach((t) => {
        const tr = document.createElement("tr");
        const isCompleted = t.status?.toLowerCase() === "completed";
        tr.innerHTML = `
          <td>${t.asset}</td>
          <td>${t.test_type || t.name}</td>
          <td>${new Date(t.date).toLocaleDateString()}</td>
          <td>${t.status}</td>
          <td>
            <button class="btn btn-continue" data-id="${t.id}">✏️ Edit</button>
            ${isCompleted ? `<button class="btn btn-send" data-id="${t.id}">📧 Send</button>` : ""}
          </td>
        `;
        tableMyTest.appendChild(tr);
      });

      // ✅ Editar test
      document.querySelectorAll(".btn-continue").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          try {
            const res = await fetch(`/form/load_test/${id}`);
            if (!res.ok) throw new Error("No se pudo cargar el test");
            const testData = await res.json();

            if (typeof window.loadExistingTest === "function") {
              window.loadExistingTest(testData);
              showSection(sectionNewTest);
            } else {
              alert("⚠️ Falta definir la función 'loadExistingTest'");
            }
          } catch (err) {
            console.error("❌ Error cargando test:", err);
            alert("❌ Error cargando datos del test.");
          }
        });
      });

      // ✅ Enviar PDF
      document.querySelectorAll(".btn-send").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
          const id = e.target.dataset.id;
          if (confirm(`¿Deseas enviar el PDF del test ID ${id}?`)) {
            try {
              const res = await fetch(`/test_done/send_pdf/${id}`, {
                method: "POST"
              });
              const data = await res.json();
              alert(data.message || "✅ PDF enviado con éxito.");
            } catch (err) {
              console.error("❌ Error enviando PDF:", err);
              alert("❌ Error enviando PDF.");
            }
          }
        });
      });

    } catch (error) {
      console.error("❌ Error loading tests:", error);
    }
  }

  // ✅ Sidebar
  btnDashboard.addEventListener("click", () => {
    showSection(sectionDashboard);
    loadChart();
  });

  btnMyTest.addEventListener("click", () => {
    showSection(sectionMyTest);
    loadMyTest();
  });

  btnNewTest.addEventListener("click", () => {
    showSection(sectionNewTest);
  });

  hamburger.addEventListener("click", () => {
    sidebar.style.display = sidebar.style.display === "block" ? "none" : "block";
  });

  // ✅ Inicio
  showSection(sectionDashboard);
  loadChart();
});
