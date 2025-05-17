document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formulario");
    form.addEventListener("submit", (event) => {
      event.preventDefault(); 
  
      const selectedValue = document.getElementById("receitas").value;
  
      sessionStorage.setItem("selectedOption", selectedValue);
  
      window.location.href = "ficha.html";
    });

    const backButton = document.querySelector(".botaoVoltar");
  
    backButton.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  });