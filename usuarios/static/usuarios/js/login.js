document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.getElementById("botaoLogin");
  
    loginButton.addEventListener("click", () => {
      const usuario = document.getElementById("usuario").value;
      const senha = document.getElementById("senha").value;
      const erroMsg = document.querySelector(".senhaErrada");
  
      if (usuario === "admin" && senha === "nimda") {
        window.location.href = "principal.html";
      } else {
        if (erroMsg) {
          erroMsg.style.display = "block";
        }
      }
    });
  });