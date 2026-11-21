// Draws the three dashboard charts from the JSON embedded by Django.
const d = JSON.parse(document.getElementById("chart-data").textContent);
const colors = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#06b6d4", "#a855f7", "#64748b"];
const make = (id, type, title, rows) => new Chart(document.getElementById(id), {
  type, data: { labels: rows.map(r => r[0]), datasets: [{ data: rows.map(r => r[1]), backgroundColor: colors, borderColor: "#6366f1" }] },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 900, easing: "easeOutQuart" },
    elements: { line: { tension: .38, borderWidth: 3 }, point: { radius: 3, hoverRadius: 6 } },
    scales: type === "doughnut" ? {} : {
      x: { grid: { display: false }, ticks: { color: "#64748b" }, border: { display: false } },
      y: { beginAtZero: true, grid: { color: "rgba(148,163,184,.14)" }, ticks: { color: "#64748b" }, border: { display: false } }
    },
    plugins: {
      legend: { display: type === "doughnut", labels: { usePointStyle: true, pointStyle: "circle", color: "#475569" } },
      title: { display: true, text: title, color: "#1e293b", font: { size: 14, weight: "700" } },
      tooltip: { padding: 12, backgroundColor: "rgba(15,23,42,.88)", cornerRadius: 10 }
    }
  } });
make("catChart", "doughnut", "Events by Category", d.cats);
make("monthChart", "line", "Monthly Registrations", d.months);
make("popChart", "bar", "Event Popularity", d.pop);
