$('.container').on('click', '.like_bt_comment', function () {
    let commentId = $(this).data('value')
    let btType = $(this).attr('id')

    $.ajax({
        url: '/comment/like-comment/',
        type: 'POST',
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': csrf,
            'like_or_dislike': btType,
            'comment_id': commentId
        },
        success: function (date) {
            let spanCount = $('#count-like-' + commentId)
            spanCount.text(String(date['count']))
            if (date['status']) {

            }
        }
    })
})


$('.comment-add').on('submit', function (e) {
    e.preventDefault()
    let commentPost = $(this).find('#text')
    let postId = $(this).find('#post_id').data('value')
    let csrf = $(this).find('input[name="csrfmiddlewaretoken"]').attr('value')
    $.ajax({
        url: '/comment/add-comment/',
        type: "POST",
        dataType: "json",
        data: {
            'csrfmiddlewaretoken': csrf,
            'post_id': postId,
            'comment_text': commentPost.val()
        },
        success: function (data) {
            if (data['status']) {
                let spanComments = $('#comment-' + postId)
                let countComments = String(parseInt(spanComments.text().split(' ')[0]) + 1)
                spanComments.text(countComments + ' Comments')
                commentPost.val('')
                $('.comment-ct-post > ul#ct-' + postId).prepend(
                    ' <li class="comment-li">\n' +
                    '     <div class="ct_likes_bar">\n' +
                    '         <button class="like_bt_comment" id="like" data-value="' + data['comment_id'] + '"><i class="ri-arrow-drop-up-line"></i></button><span id="count-like-' + data['comment_id'] + '">0</span><button class="like_bt_comment" id="dislike" data-value="' + data['comment_id'] + '"><i class="ri-arrow-drop-down-line"></i></button>' +
                    '     </div>\n' +
                    '     <div class="meta_com_data">\n' +
                    '         <div class="profile-photo">\n' +
                    '              <img src="'+ data['ava_user'] +'" alt="" class="media media-obj">\n' +
                    '         </div>\n' +
                    '     </div>\n' +
                    '     <div class="content-ct-comment">\n' +
                    '         <a href="'+ data['link'] +'">@' + data['username'] + '</a>\n' +
                    '         <span class="content-comment">' + data['comment_text'] + '</span>\n' +
                    '    </div>\n' +
                    ' </li>'
                )
            }
        }
    })
})
