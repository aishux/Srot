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