$('#whatsapp_button').tooltip({placement: 'left',trigger: 'manual'}).tooltip('show');
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

function sendWhatsapp(data) {
			let isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
			if (isMobile) {
				window.open(`whatsapp://send?phone=14155238886&text=${data}`)
			}
			else {
				window.open(`https://web.whatsapp.com:/send?phone=14155238886&text=${data}`)
			}
		}