function formCheck(){
    if($("#signup_pass1").val() == $("#signup_pass2").val()){
        document.getElementById("password-mismatch").hidden = true
        $.ajax({
            type: 'GET',
            url: '/signup/',
            data: {
                'username':$('#signup_username').val()
            },
            success: function(data){
                if(data.exists == "no"){
                    $("#signupForm").submit()
                }
                else{
                    document.getElementById("username-unavailable").hidden = false
                }
            }
        })
    }
    else{
        document.getElementById("password-mismatch").hidden = false
    }
}