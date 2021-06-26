// Get the modal
var modalDelete = document.getElementById("myModalDelete");

// Get the button that opens the modal
var btnDelete = document.getElementById("myBtnDelete");

// Get the <span> element that closes the modal
var spanDelete = document.getElementsByClassName("closeBtn")[0];

// When the user clicks the button, open the modal 
btnDelete.onclick = function() {
  modalDelete.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanDelete.onclick = function() {
  modalDelete.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalDelete) {
    modalDelete.style.display = "none";
  }
}