function _(el){
    return document.getElementById(el)
}
// Profile Page Validation
REGX= {
    'nameREGX':/^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/,
    'emailREGX':/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i,
    'phone_number':/^\+(91)[6-9]\d{9}$/g,
    'description_check':/^.{100,}/,
    'username':/^.{4,16}/,
    'uniqueIdREGX':/^.{7,15}/
}

function signUpPageValidation(){
    errors = [];
    var username = document.querySelector('input[name="username"]').value;
    var password =document.getElementsByName('password1')[0].value;
    var confirm_password = document.getElementsByName('password2')[0].value;
    var first_name = document.querySelector('input[name="first_name"]').value;
    var last_name = document.querySelector('input[name="last_name"]').value;
    var email = document.querySelector('input[name="email"]').value;
    var usernameCheck = REGX['username'].test(username);
    if(!usernameCheck){
        errors.push('Username must be between 4 to 16 characters long.');
    }
    var firstNameCheck = REGX['nameREGX'].test(first_name);
    if(!firstNameCheck){
        errors.push('First name should not contain any special character or digit.');
    }
    var lastNameCheck = REGX['nameREGX'].test(last_name);
    if(!lastNameCheck){
        errors.push('Last name should not contain any special character or digit.');
    }
    var emailCheck =  REGX['emailREGX'].test(email);
    if(!emailCheck){
        errors.push('Please enter a valid email.');
    }
    if (password != confirm_password){
        errors.push('Password and Confirm Password are different.');
    }
    txt = ""
    errors.forEach(signUpErrors);
    if(txt === "") return true;
    else{
        _('error-log').innerHTML = txt;
        return false;
    }
}
function signUpErrors(value, index, array) {
    txt = txt + '<li style="color:red;font-weight:bold;font-size:0.85em;">*' + value + '</li>'
}

function logInPageValidation(){
    var username = document.querySelector('input[name="username"]').value;
    var usernameCheck = REGX['username'].test(username);
    if(!usernameCheck){
        _('login-error').innerHTML = '<p style="color:red;">Username must be between 8 to 16 characters long</p>';
        return false;
    }
    return true;
}

function TogglePassword(){  
    var x = document.querySelector('input[name="password1"]');
    var y = document.querySelector('input[name="password2"]');
    if (x.type === "password" && y.type === "password") {
        x.type = "text";
        y.type="text";
    } else {
        x.type = "password";
        y.type = 'password';
    }
}
function logInPasswordToggle(){
    var x = document.querySelector('input[name="password"]');
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
function changePassword(){
    var x = document.querySelector('input[name="old_password"]');
    var y = document.querySelector('input[name="new_password1"]');
    var z = document.querySelector('input[name="new_password2"]');
    if (x.type === "password" && y.type === "password" && z.type=="password") {
        x.type = "text";
        y.type="text";
        z.type="text";
    } else {
        x.type = "password";
        y.type = 'password';
        z.type = "password";
    }
}

function validateAddSubject(){
    var teacher = document.getElementsByName('teacher')[0].value;
    if(teacher=='Please Choose')  return false;
    else return true;
}
function validateprofile(){
    var phoneNumber = document.querySelector("input[name='phone_number']").value;
    var whatsapp_number= document.querySelector("input[name='whatsapp_number']").value;
    var phoneRGEX =/^\+(91)[6-9]\d{9}$/g;
    var phoneResult = phoneRGEX.test(phoneNumber);
    var phoneRGEX =/^\+(91)[6-9]\d{9}$/g;
    var whatsapp = phoneRGEX.test(whatsapp_number);
    txt = "";
    if(!phoneResult){
        txt += "Phone no. must be valid Indian phone number.<br>";
    }
    if(!whatsapp){
        txt += 'Whatsapp no. must be valid indian phone numbe.<br>';
    }
    txt = '<p style="color:red;text-align:center;">'+ txt + '</p>'
    _('profile-errors').innerHTML = txt;
    if(phoneResult && whatsapp) return true;
    else return false;
}
function forgotPasswordValidate(){
    var email = document.getElementsByName('email')[0].value;
    var emailCheck =  REGX['emailREGX'].test(email);
    if(!emailCheck){
        txt="You have entered a non-valid email.";
        document.getElementById('password-reset-error').textContent = txt;
        return false;
    }
    return true;
}
function uniqueid(){
    var uniqueId = document.getElementsByName('join_key')[0].value;
    var uniqueIdCheck =  REGX['uniqueIdREGX'].test(uniqueId);
    if(!uniqueIdCheck){
        txt="Unique id would have 7 to 15 characters.";
        document.getElementById('uniqueIdCheck-error').textContent = txt;
        return false;
    }
    return true;
} 

const actualBtn = _('actual-btn');
const fileChosen = _('file-chosen');
if(actualBtn != null){
    actualBtn.addEventListener('change', function(){
        try {
            var maxFileSize = 25
            var fileSize = _('actual-btn').files[0].size
            fileSize = fileSize / 1048576;
            if(fileSize <= maxFileSize ){
            _('file-upload-label').textContent = this.files[0].name + " selected. Click again to change"
            }
            if (fileSize > maxFileSize) throw "Too big";
            }
            catch (e) {
            alert("Sorry, file is too large. Please select one that is smaller than "+maxFileSize +' Mb');
            e.preventDefault()
            console.log(_('actual-btn').files[0].size);
            _('file-upload-label').innerHTML='Upload File<span>\
            <i class="fa mx-2 fa-upload" aria-hidden="true"></i></span></label>';
            }
        })
}

const txa = document.getElementsByTagName('textarea');
for (let i = 0; i < txa.length; i++) {
    try{
        txa[i].setAttribute('style', 'height:' + (txa[i].scrollHeight) + 'px;overflow-y:hidden;');
        txa[i].addEventListener("input", OnInput, false);
    }catch(err){
        message="Not on that page."
    }
}