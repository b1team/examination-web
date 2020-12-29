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
  var vali_editor = document.forms["formQuestion"]["question"].value;
  if (vali_editor =="" || vali_editor ==null) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkAnswer(input) {
  var vali_answer_a = document.forms["formQuestion"]["answerA"].value;
  var vali_answer_b = document.forms["formQuestion"]["answerB"].value;
  var vali_answer_c = document.forms["formQuestion"]["answerC"].value;
  var vali_answer_d = document.forms["formQuestion"]["answerD"].value;
  if (vali_answer_a == "" || vali_answer_a == null || vali_answer_b == "" || vali_answer_b == null|| 
  vali_answer_c== "" || vali_answer_c == null || vali_answer_d == "" || vali_answer_d == null) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkAnswerKey(input) {
  var vali_key = document.forms["formname"]["ratingInput1"].value;
  if (vali_key < 0) {
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