'use-stric'

$(document).ready(function() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // const csrftoken = getCookie('csrftoken');



    // Comment AJAX call.

    $('#commentButton').click(function(e) {
        e.preventDefault();

        const formData = $('#commentForm').serialize();
        console.log(formData);
        $.ajax({
            url: $('#commentForm').data('url'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function(res) {
                
                $('#comments-list').append(
                    `<div class="comment-info-container" id="comment-${res.id}">
                        <p class="comment-info comment-writer-time">${res.username} | jetzt</p>
                        <p class="comment-content comment-new-content">${res.comment}</p>
                        <hr>
                    </div>
                    `  
                )
            
            },
            error: function(err){
                if(err.responseJSON.url) {
                    console.log(err)
                    alert('Sie brauchen einzuloggen');
                    window.location.replace(err.responseJSON.url);
                } else {
                    alert('Etwas ist schief gelaufen')
                    console.log(err)
                }
                                
            }

        })

    });


    // HomePage topics toggle, Show All and Close All.

    $('#topicsToggle').click(function(e) {
        e.preventDefault();

        const toggleTxt = $(this).text();
        
        if (toggleTxt == 'Show All') {
            $(this).text('Close All');
            $('.collapse').addClass('show');

        } else if (toggleTxt == 'Close All') {
            $(this).text('Show All');
            $('.collapse').removeClass('show');
        }
    });


    // REPLY BUTTON CLICK EVENT

    $(".commentReplyButton").on("click", function() {
        
        // postID - To send formData to correct post, which means current post.
        // commentID - To insert form into correct position, which is the comment users like to reply to.
        // csrfToken - To get a current csrftoken to send a form with.
        var postID = $(this).data('postid');
        var commentID = $(this).data('id');
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        
        if($(document).find('#replyCommentForm')) {
            $('#replyCommentForm').remove();
            $('#replyCloseButton').remove();
        } 

        // Editing, form id, Options to be selected automatically.
        $(`#comment-${commentID}`).append(`
        <button class="btn btn-sm btn-outline-danger float-right mt-2 mb-2 text-monospace" id="replyCloseButton">Abbrechen</button>
        <form data-url="/post/${postID}/addcomment/" id="replyCommentForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"></input>
            <div id="div_id_comment" class="form-group text-monospace"> <label for="id_comment" class=" requiredField">
                            Kommentar<span class="asteriskField">*</span> </label> <div class=""> <textarea name="comment" cols="40" rows="10" summernote="{'width': '100%', 'height': '450', 'toolbar': [['style', []], ['font', ['bold', 'underline']], ['fontname', []], ['color', ['color']], ['insert', ['link']]]}" maxlength="1000" class="summernotewidget form-control" id="id_comment" hidden="true" style="display: none;"></textarea><script>
            var settings_id_comment = {"width": "100%", "height": "280", "lang": "en-US", "toolbar": [["style", []], ["font", ["bold", "underline"]], ["fontname", []], ["color", ["color"]], ["insert", ["link"]]], "url": {"language": "/static/summernote/lang/summernote-en-US.min.js", "upload_attachment": "/summernote/upload_attachment/"}};
            </script>
            <style>
            iframe.note-fullscreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw!important;
            height: 100vh!important;
            z-index: 4000;
            }
            </style>
            <div class="summernote-div" cols="40" maxlength="1000" rows="10" summernote="{'width': '100%', 'height': '450', 'toolbar': [['style', []], ['font', ['bold', 'underline']], ['fontname', []], ['color', ['color']], ['insert', ['link']]]}" width="100%" height="450"> <iframe id="id_comment_iframe" src="/summernote/editor/id_comment/" frameborder="0" width="100%" height="450" style="height: 450px;"></iframe>
            </div> </div> </div> <div id="div_id_parent" class="form-group"> <div class=""> 
            <select name="parent" class="d-none select form-control" id="reply_id_parent">
            <option value="${commentID}" selected="${commentID}"></option>
            </select>
            <button class="btn btn-sm btn-outline-dark" type="submit" id="replyCommentButton">Kommentieren</button>
                
        </form>`)


        // replay comment ajax call
        // if This ajax call is outside of reply ajax, it won't work at all. it doesn't recognize the button clicked.

        $('#replyCommentButton').on('click', function (e) {
            e.preventDefault();
            
            const replyFormData = $('#replyCommentForm').serialize();

            $.ajax({
                url: $('#replyCommentForm').data('url'),
                type: 'POST',
                data: replyFormData,
                success: function (res) {
                    // console.log(`Comment IDDDD ${commentID}`)
                    $(`#comment-${commentID}`).append(
                        `<div class="comment-info-container pl-3" id="comment-${res.id}">
                            <p class="comment-info comment-writer-time">${res.username} | jetzt</p>
                            <p class="comment-content comment-new-content">${res.comment}</p>
                        </div>
                        <hr>
                        `
                        
                    )

                },
                error: function(err){
                    if(err.responseJSON.url) {
                        console.log(err)
                        alert('Sie brauchen einzuloggen');
                        window.location.replace(err.responseJSON.url);
                    } else {
                        alert('Etwas ist schief gelaufen')
                        console.log(err)
                    }
                                    
                }

            })
            $('#replyCommentForm').remove();
            $('#replyCloseButton').remove();

        })
        // Reply Form Close Button
        $('#replyCloseButton').click(function () {
            $('#replyCommentForm').remove();
            $('#replyCloseButton').remove();
        })

    });


    // Comment show all close all
    $('#commentOpenCloseButton').on('click', function () {
        // console.log($(this)[0].innerText)
        if($(this)[0].innerText == 'Schließen') {
            $('#mpttComments').hide();
            $('#replyCommentForm').remove();
            $('#replyCloseButton').remove();
            $(this)[0].innerText = 'Öffnen';
        } else if ($(this)[0].innerText == 'Öffnen') {
            $('#mpttComments').show();
            $(this)[0].innerText = 'Schließen'
        }

    })
    // Comment show all close all ends


    // Post Like Ajax call
    $('#likeIcon').click(function (e) {
        e.preventDefault();

        const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        const postID = $(this).data('postid');

        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data:{
                csrfmiddlewaretoken: csrfToken,
                post_id: postID,
                action: 'post',
            },
            success: function (res) {
                
                if(res.result == 'plus') {
                    $('#likeIcon').css('color', '#eb4034')
                    $('#like-counts').text(`${res.count} Up`)
                    $('#post-info-ups').text(`${res.count} Up`)
                } else if(res.result == 'minus') {
                    $('#likeIcon').css('color', 'grey')
                    $('#like-counts').text(`${res.count} Up`)
                    $('#post-info-ups').text(`${res.count} Up`)
                } else if(res.result == 'false') {
                    alert('Sie brauchen einzuloggen')
                }

            },
            error: function (xhr, errmsg, err) {

            }
        })
        
    })



    // topic favorite ajax call
    $('#favorite-topic').click(function (e) {
        e.preventDefault();
        
        // Since topic-favorite view doesn't provide csrf token, it should fetch the token from cookies.
        // on the top of this js file, the function to fetch the csrf_token is located, which is specified in django docs.
        const csrftoken = getCookie('csrftoken');
        const topicSlug = $(this).data('topicslug');
        
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data:{
                csrfmiddlewaretoken: csrftoken,
                topic_slug: topicSlug,
                action: 'post',
            },
            success: function (res) {
                
                if(res.result == 'added') {
                    $('#favorite-topic').html('<i class="fas fa-star" style="color: rgb(255, 94, 0);"></i>');
                } else if (res.result == 'removed') {
                    $('#favorite-topic').html('<i class="far fa-star"></i>');
                }
            },
            error: function (xhr, errmsg, err) {

            }
        })
    })



    $('.requestRecommandation').click(function(e) {
        e.preventDefault();
        console.log('clicked')

        const csrftoken = getCookie('csrftoken');
        const requestID = $(this).data('requestid');
        console.log(requestID);

        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken,
                request_id: requestID,
            },
            success: function (res) {
                console.log(res)
                if(res.result == 'plus') {
                    $(`#recommendation${res.request_id}`).html('<i class="far fa-thumbs-up" style="color: #eb4034"></i>')
                } else if(res.result == 'minus') {
                    $(`#recommendation${res.request_id}`).html('<i class="far fa-thumbs-up"></i>')
                }
            },
            error: function (xhr, errmsg, err) {

            }
        })

    })

});
