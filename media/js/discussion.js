// Apply active class to whichever filters are applied

if (window.location.href.includes("tags")) {
    var params = window.location.href.split("?")[1].split("&")
    if (params.length == 2) {
        $(".no_filter").removeClass("active")
        params = params[1].split("=")[1].split(",")
        for (let i = 0; i < params.length; i++) {
            try {
                $(`.${params[i].toLowerCase()}_filter`).addClass("active")
            } catch (error) {
                continue
            }
        }
        $(".no_filter").hide()
    }
}
else{
    $(".no_filter").addClass("active")
    $(".no_filter").show()
}


try { Typekit.load({ async: true }); } catch (e) { }


$(document).ready(function () {

    var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        maxItemCount: 15,
        searchResultLimit: 15,
        renderChoiceLimit: 15
    });

});

function showComments(dis) {
    if ($(`#CommentPanel${dis}`).children().length == 4) {
        $.ajax({
            type: 'GET',
            url: '/showComments/',
            data: {
                'dis_id': dis,
            },
        })
            .success(function (data) {

                if (data.has_comments == "yes") {

                    all_coms = JSON.parse(data.all_comments)
                    for (i = 0; i < all_coms.length; i++) {
                        $(`#CommentPanel${dis}`).append(`
                            <div class="comment-post">
                                <div class="comment-img"><img
                                        src="https://cdn.iconscout.com/icon/free/png-256/avatar-372-456324.png" />
                                </div>
                                <div class="comment-details">
                                    <p><span class="comment-author">${all_coms[i].fields.user}</span></p>
                                    <p class="comment-content">${all_coms[i].fields.comment}</p>
                                </div>
                            </div>
                            `)
                    }
                    $(`#CommentPanel${dis} h5`).html(`Total Comments (${all_coms.length})`)
                }
            })
    }
}


function saveComment(dis) {
    given_comment = $(`#comment_area${dis}`)
    $.ajax({
        type: 'GET',
        url: '/saveDComment/',
        data: {
            'dis_id': dis,
            'comment': given_comment.val()
        },
    })
        .success(function (data) {
            $(`#CommentPanel${dis}`).append(`
            <div class="comment-post">
                <div class="comment-img"><img
                        src="https://cdn.iconscout.com/icon/free/png-256/avatar-372-456324.png" />
                </div>
                <div class="comment-details">
                    <p><span class="comment-author">${data.user_name}</span></p>
                    <p class="comment-content">${given_comment.val()}</p>
                </div>
            </div>
            `)
            given_comment.val("")
        })
}

function applyFilter(filt, class_status) {
    var current_url = window.location.href
    if (!current_url.includes("page")) {
        current_url = current_url + "?page=1"
    }
    current_url = current_url.split("?")
    var get_params = current_url[1].split("&")
    var page_no = 1
    var flag = 0

    // For Toggling between helping and needhelp

    if (get_params.length == 2) {
        var toggle_status = get_params[1].split("=")[1]
        if(filt == "Helping" && toggle_status.includes("Needhelp")){
            flag = 1
            if(toggle_status.includes(",Needhelp")){
                toggle_status = toggle_status.replace(",Needhelp", "")
            }
            else{
                if (toggle_status.includes("Needhelp,")) {
                    toggle_status = toggle_status.replace("Needhelp,", "")
                }
                else{
                    toggle_status = toggle_status.replace("Needhelp", "")
                }
            }
        }
        else{
            if(filt == "Needhelp" && toggle_status.includes("Helping")){
                flag = 1
                if(toggle_status.includes(",Helping")){
                    toggle_status = toggle_status.replace(",Helping", "")
                }
                else{
                    if (toggle_status.includes("Helping,")) {
                        toggle_status = toggle_status.replace("Helping,", "")
                    }
                    else{
                        toggle_status = toggle_status.replace("Helping", "")
                    }
                }
            }
        }
    }


    // If the filter is applied and now we want to remove filter
    if (class_status.className.includes("active")) {

        // Get the tags used from the url and remove the filter requested by replacing it with empty string

        tags_used = get_params[1].split("=")[1]

        if(tags_used.includes(","+filt)){
            tags_used = tags_used.replace(","+filt, "")
        }
        else{
            if (tags_used.includes(filt+",")) {
                tags_used = tags_used.replace(filt+",", "")
            }
            else{
                tags_used = tags_used.replace(filt, "")
            }
        }
        
        // If there are no tags used then remove the tags parameter from the url

        if (tags_used != "") {
            next_url = (current_url[0] + `?page=${page_no}&tags=${tags_used}`)
        }

        // Else pass the remaining tags
        else {
            next_url = (current_url[0] + `?page=${page_no}`)
        }

        // Now move to the next url with the page number and filters

        window.location.replace(next_url)
    }

    // If we want to apply a filter
    else {

        var tags_used = null

        // Check if there is tags parameter present in the url

        if (get_params.length == 2) {

            // Get the tags/filters that are in use

            // Check for the toggle status

            if(flag == 1){
                tags_used = toggle_status
            }
            else{
                tags_used = get_params[1].split("=")[1]
            }
        }

        // If there are no tags present then we add the tags parameter as well with our filter

        if (tags_used == null || tags_used == "") {
            next_url = (current_url[0] + `?page=${page_no}&tags=${filt}`)
            window.location.replace(next_url)
        }

        else {

            // If there are already some tags present then we add this filter to them

            next_url = (current_url[0] + `?page=${page_no}&tags=${tags_used},${filt}`)
            window.location.replace(next_url)
        }
    }
}

// Function for pagination to work
function changePage(pageNo){
    if (window.location.href.includes("?")) {
        var main_url = window.location.href.split("?")
        var used_tags = main_url[1].split("&")[1]
        if(used_tags != undefined){
            window.location.replace(main_url[0] + `?page=${pageNo}`+ `&${used_tags}`)
        }
        else{
            window.location.replace(main_url[0] + `?page=${pageNo}`)
        }
    }
    else{
        window.location.replace(window.location.href + `?page=${pageNo}`)
    }
}

function LoginAlert(){
    alert("Please Login to Contribute!")
}