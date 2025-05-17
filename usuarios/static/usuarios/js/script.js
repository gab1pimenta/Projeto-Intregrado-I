document.addEventListener("DOMContentLoaded", () => {
    const selectedOption = sessionStorage.getItem("selectedOption");
    const resultElement = document.getElementById("receitaEscolhida");
    resultElement.textContent = selectedOption;

    const backButton = document.querySelector(".botaoVoltar");
  
    backButton.addEventListener("click", () => {
      window.location.href = "principal.html";
    });
  });