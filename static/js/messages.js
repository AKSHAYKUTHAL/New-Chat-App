let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'ws://' 

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    console.log(e.data)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
	    message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send">8:55 AM, Today</span>
				</div>
				<div class="img_cont_msg">
					<img src="">
				</div>
			</div>
	    `
    }
	else{
	    message_element = `
           <div class="d-flex mb-4 received">
              <div class="img_cont_msg">
                 <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
              </div>
              <div class="msg_cotainer">
                 ${message}
              <span class="msg_time">8:40 AM, Today</span>
              </div>
           </div>
        `

    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    message_body.scrollTop(message_body[0].scrollHeight);
	input_message.val(null);
}


$('.contact-li').on('click', function (){
    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}






// auto suggestion of useers 

$(document).ready(function(){
    $('.search').keyup(function(){
        // console.log("Searching for:", $(this).val());
        let query = $(this).val();
        if (query != '') {
            $.ajax({
                url: "/chat/search_users/",
                method: "GET",
                data: {query: query},
                success: function(data) {
                    // console.log("Received data:", data); 
                    let usersList = '<ul class="list-group">';
                    $.each(data, function(index, user){
                        usersList += `<li class="list-group-item user-suggestion" data-user-id="${user.id}">${user.username}</li>`;
                    });
                    usersList += '</ul>';
                    $('.search-results').html(usersList);
                }
            });
        } else {
            $('.search-results').html('');
        }
    });

        // csrf token retrieval function

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        const csrftoken = getCookie('csrftoken');
        
        $(document).on('click', '.user-suggestion', function(){
            let selectedUserId = $(this).data('user-id');
            $.ajax({
                url: "/chat/create_thread/",
                method: "POST",
                data: {
                    'selected_user_id': selectedUserId,
                    'csrfmiddlewaretoken': csrftoken
                },
                success: function(response) {
                    console.log('Thread created with ID:', response.thread_id);
                    if(response.redirect_url) {
                        window.location.href = response.redirect_url;
                    }
                }
            });
        });
});