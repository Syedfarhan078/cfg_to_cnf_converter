async function convertGrammar() {
  const grammarText = document.getElementById("grammarInput").value;
  let grammar;
  try {
    grammar = JSON.parse(grammarText);
  } catch (e) {
    alert("Invalid JSON format!");
    return;
  }

  const res = await fetch("/convert", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(grammar)
  });

  const data = await res.json();
  document.getElementById("output").textContent = JSON.stringify(data.cnf, null, 2);
}
