// Profile Page Validation
REGX= {
    'nameREGX':/^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/,
    'emailREGX':/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i,
    'phone_number':/^\+(91)[6-9]\d{9}$/g,
    'description_check':/^.{100,}/,
    'username':/^.{8,16}/
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
        errors.push('Username must be between 8 to 16 characters long.');
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