async function runAgent() {
  const task = document.getElementById("task").value;
  const log = document.getElementById("log");
  const screen = document.getElementById("screen");

  log.textContent = "Ejecutando agente...\n";

  const res = await fetch("/api/run-agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task })
  });

  const data = await res.json();

  log.textContent = data.logs || "Sin logs";

  // Mostrar capturas como frames
  let i = 0;
  const frames = data.screenshots || [];

  const interval = setInterval(() => {
    if (i >= frames.length) {
      clearInterval(interval);
      return;
    }
    screen.src = frames[i];
    i++;
  }, 800);
}
