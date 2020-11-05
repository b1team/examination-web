
// validate register 
const form = document.getElementById('form-register');
const usernameField = document.getElementById('username');
const password = document.getElementById('password');
const password2 = document.getElementById('password2');
const email = document.getElementById('email');
const phone = document.getElementById('phone');
const age = document.getElementById('age');
const sex = document.getElementById('sex');
const classify = document.getElementById('classify');
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



// Check required fields
function checkRequired(inputArr) {
  inputArr.forEach(function(input) {
    if (input.value.trim() === '') {
      showError(input, `${getFieldName(input)} is required`);
    } else {
      showSuccess(input);
    }
  });
}

// Check input length
function checkLength(input, min, max) {
  if (input.value.length < min) {
    showError(
      input,
      `${getFieldName(input)} must be at least ${min} characters`
    );
  } else if (input.value.length > max) {
    showError(
      input,
      `${getFieldName(input)} must be less than ${max} characters`
    );
  } else {
    showSuccess(input);
  }
}
function checkPhone(input,max){
    if (input.value.length < max) {
        showError(
          input,
          `${getFieldName(input)} must be at least ${max} characters`
        );
      } else if (input.value.length > max) {
        showError(
          input,
          `${getFieldName(input)} must be equal ${max} characters`
        );
      } else {
        showSuccess(input);
      }
}
// Check passwords match
function checkPasswordsMatch(input1, input2) {
  if (input1.value !== input2.value) {
    showError(input2, 'Passwords do not match');
  }
}

// Get fieldname
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}
function checkEmail(input){
    if(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email.value)){
        showSuccess(input);
    }
    else{
        showError(input);
    }
}
// Event listeners
form.addEventListener('submit', function(e) {
  e.preventDefault();

  checkRequired([usernameField, password, email, password2, phone, age, sex, classify]);
  checkLength(usernameField, 6, 15);
  checkLength(password, 6, 25);
  checkPhone(phone, 11);
  checkLength(age, 1, 2);
  checkEmail(email);
  checkPasswordsMatch(password, password2);
});
