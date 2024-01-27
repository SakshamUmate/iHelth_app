function detectErrors() {
  var inputText = document.getElementById("textInput").value;
  var errors = detectErrorsSimple(inputText);
  displayErrors(errors);
}

function detectErrorsSimple(text) {
  var errors = [];
  if (text.toLowerCase().includes("error")) {
    errors.push("The word 'error' is detected in the text.");
  }
  return errors;
}

function displayErrors(errors) {
  var errorList = document.getElementById("errorList");
  errorList.innerHTML = "";
  errors.forEach(function (error) {
    var listItem = document.createElement("li");
    listItem.textContent = error;
    errorList.appendChild(listItem);
  });
}
