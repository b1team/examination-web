//form validate create room
const form_create_exam = document.getElementById("formExam");
const duration = document.getElementById("duration");
const num = document.getElementById("num");
const num_easy = document.getElementById("num_easy");
const num_med = document.getElementById("num_med");
const num_hard = document.getElementById("num_hard");

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
function checkDuration(input) {
  if (input.value =="" || input.value ==null) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkNumberQuestion(input) {
  if (input.value == "" || input.value == null ) {
    showError(
      input,
      `${getFieldName(input)} must be empty!!!`
    );
  }
}
function checkTotalQuestion(input1, input2, input3, input4) {
  if (input1.value + input2.value + input3.value != input4.value) {
    showError(
      input,
      `${getFieldName(input)} must be not equal!!!`
    );
  }
}
// Event listeners
form_create_exam.addEventListener('submit', function () {
  checkDuration(duration);
  checkNumberQuestion(num);
  checkTotalQuestion(num_easy, num_med, num_hard, num);
});