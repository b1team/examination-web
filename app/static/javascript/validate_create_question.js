//form validate create room
const form_create_room = document.getElementById("formQuestion");
const editor = document.getElementById("test-editor");
const answer = document.getElementById("answer");
const answer_key = document.getElementById("answerKey");

// Show input error message
function showError(input, message) {
  const formControl = input.parentElement;
  formControl.className = 'form-Control error';
  const small = formControl.querySelector('small');
  small.innerText = message;
}

// Show success outline
function showSuccess(input) {
  const formControl = input.parentElement;
  formControl.className = 'form-Control success';
}
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}
function checkEditor(input) {
  if (input.value =="" || input.value ==null) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkAnswer(input) {
  if ( input.value == null || input.value == "") {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkAnswerKey(input) {
  if (input.value< 0) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
// Event listeners
form_create_room.addEventListener('submit', function () {
  checkEditor(editor);
  checkAnswer(answer);
  checkAnswerKey(answer_key);
});