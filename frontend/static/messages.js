function fetchdata(){
    $.ajax({
        url: '/messages',
        type: 'get',
        success: function(messages) {
            if (messages) {
                let textArea = $('#mTextArea');
                for (message of messages.split(' | ')) {
                    textArea.val(message + '\n' + textArea.val());
                }
            }
        }
    });
}

$(document).ready(function(){
    setInterval(fetchdata, 3000);
});