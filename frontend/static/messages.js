function fetchdata(){
    $.ajax({
        url: '/messages',
        type: 'get',
        success: function(messages) {
            if (messages) {
                let textArea = $('#mTextArea');
                for (message of messages.split(' | ')) {
                    textArea.val(textArea.val() + message + '\n');
                }
            }
        }
    });
}

$(document).ready(function(){
    setInterval(fetchdata, 3000);
});