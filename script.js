function add(author, text) {
  const div = document.createElement("div");
  div.innerText = `${author}: ${text}`;
  document.getElementById("messages").appendChild(div);
}

async function send() {
  const input = document.getElementById("input");
  const message = input.value.trim();
  if (!message) return;

  add("Vous", message);
  input.value = "";

  const res = await fetch("/api/app", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  add("IA", data.reply || "Erreur");
}