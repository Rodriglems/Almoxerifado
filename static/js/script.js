document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("pesquisa");
  const sugestoesEl = document.getElementById("sugestoes");
  if (!input || !sugestoesEl) return;

  let timeout = null;
  input.addEventListener("input", function () {
    clearTimeout(timeout);
    const termo = this.value.trim();
    if (termo.length < 2) {
      sugestoesEl.innerHTML = "";
      return;
    }
    timeout = setTimeout(() => {
      fetch(`/autocomplete-funcionario/?q=${encodeURIComponent(termo)}`)
        .then((response) => {
          if (!response.ok) throw new Error("Requisição falhou");
          return response.json();
        })
        .then((data) => {
          sugestoesEl.innerHTML = data
            .map(
              (item) =>
                `<div class="sugestao-item" data-id="${item.id}">${escapeHtml(
                  item.nome
                )}</div>`
            )
            .join("");
        })
        .catch((err) => {
          console.error("Erro autocomplete:", err);
          sugestoesEl.innerHTML = "";
        });
    }, 250);
  });

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (m) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[m];
    });
  }
});
