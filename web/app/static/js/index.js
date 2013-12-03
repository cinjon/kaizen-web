function showLogin() {
    $("#registerForm").hide();
    $("#loginForm").show();
    $("#toggleLoginSignup").val("Sign Up");
    $("#toggleLoginSignup").attr("onClick", "showRegistration()");
}

function showRegistration() {
    $("#registerForm").show();
    $("#loginForm").hide();
    $("#toggleLoginSignup").val("Login");
    $("#toggleLoginSignup").attr("onClick", "showLogin()");
}