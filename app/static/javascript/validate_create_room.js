//form validate create room
const form_create_room = document.getElementById("formCreateRoom");
const classname = document.getElementById("classname");
const subject = document.getElementById("subject");
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

function checkClassname(input){
    if(input.value == "" || input.value == null){
      showError(
        input,
        `${getFieldName(input)} must be empty !!!`
      );
    }
}
function checkSubject(input){
  if(input.value == "" || input.value == null){
    showError(
      input,
      `${getFieldName(input)} must be empty !!!`
    );
  }
}
form_create_room.addEventListener('submit', function() {
  checkClassname(classname);
  checkSubject(subject);
});