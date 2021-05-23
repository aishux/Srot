function changeLead(page_no=1){
    val = document.getElementById("service_filter").value
    our_url = window.location.protocol+"//"+window.location.host
    city_val = document.getElementById("state").value
    state_val = document.getElementById("sts").value
    if(val == "Food Supplier"){
        if (state_val=="" && city_val=="") {
            window.location.href = our_url + `/leads/foodleads/${page_no}`
        }
        else{
            window.location.href = our_url + `/leads/${val}/${state_val}/${page_no}/${city_val}`
        }
    }
    else if(val == "Beds"){
        if (state_val=="" && city_val=="") {
        window.location.href = our_url + `/leads/bedleads/${page_no}`
        }
        else{
            window.location.href = our_url + `/leads/${val}/${state_val}/${page_no}/${city_val}`
        }
    }
    else if(val == "injections"){
        if (state_val=="" && city_val=="") {
        window.location.href = our_url + `/leads/injectionleads/${page_no}`
        }
        else{
            window.location.href = our_url + `/leads/${val}/${state_val}/${page_no}/${city_val}`
        }
    }
    else if(val == "Oxygen"){
        if (state_val=="" && city_val=="") {
        window.location.href = our_url + `/leads/oxygenleads/${page_no}`
        }
        else{
            window.location.href = our_url + `/leads/${val}/${state_val}/${page_no}/${city_val}`
        }
    }
    else if(val == "Plasma Donor"){
        if (state_val=="" && city_val=="") {
        window.location.href = our_url + `/leads/plasmaleads/${page_no}`
        }
        else{
            window.location.href = our_url + `/leads/${val}/${state_val}/${page_no}/${city_val}`
        }
    }
}