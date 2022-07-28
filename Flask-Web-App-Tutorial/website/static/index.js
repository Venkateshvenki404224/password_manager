function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}
function passdelete(passId) {
  fetch("/delete", {
    method: "POST",
    body: JSON.stringify({ passId: passId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function passedit(passId) {
  fetch("/update", {
    method: "POST",
    body: JSON.stringify({ passId: passId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
var password=document.getElementById("password1","password2");
function genPassword() {
    var chars = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var passwordLength = 12;
    var password = "";
 for (var i = 0; i <= passwordLength; i++) {
   var randomNumber = Math.floor(Math.random() * chars.length);
   password += chars.substring(randomNumber, randomNumber +1);
  }
        document.getElementById("password1").value = password;
        document.getElementById("password2").value = password;
 }
var password=document.getElementById("psw");
function Password() {
    var chars = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var passwordLength = 12;
    var password = "";
 for (var i = 0; i <= passwordLength; i++) {
   var randomNumber = Math.floor(Math.random() * chars.length);
   password += chars.substring(randomNumber, randomNumber +1);
  }
        document.getElementById("psw").value = password;
 }
var table = document.getElementById("table"),rIndex;
for(var i =1 ; i<table.rows.length;i++)
{
    table.rows[i].onclick=function ()
    {
        rIndex=this.rowsIndex;
        console.log(rIndex);

        document.getElementById("")

    }
}
