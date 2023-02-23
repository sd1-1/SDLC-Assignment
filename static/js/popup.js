

function closeAllForms(){

  document.getElementById("uploadForm").style.display = "none";
  document.getElementById("updateForm").style.display = "none";
  document.getElementById("deleteForm").style.display = "none";
}


function openForm(formName) {
    closeAllForms()
    document.getElementById(formName).style.display = "flex";
}
  

function closeForm(formName) {
    document.getElementById(formName).style.display = "none";
}