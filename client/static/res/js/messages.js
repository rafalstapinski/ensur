// var send_message = function(receiver, pubkey, message) {
//   options = {
//     data: message,
//     publicKeys: openpgp.key.readArmored(pubkey).keys,
//   }
//
//   openpgp.encrypt(options).then(function(ciphertext) {
//     encrypted_message = ciphertext.data
//
//     options = {
//       data: message,
//       publicKeys: openpgp.key.readArmored(localStorage.getItem('pubkey')).keys,
//     }
//
//     openpgp.encrypt(options).then(function(ciphertext) {
//
//
//       $.ajax({
//         type: 'post',
//         url: 'http://localhost:8080/message/new',
//         data: {
//           receiver: receiver,
//           sender: Cookies.get('username'),
//           message: encrypted_message,
//           copy: encrypted_copy
//         },
//         success: function(data) {
//           if (data['status'] == 200) {
//             $('#receiver').val('')
//             $('#message_box').val('')
//           } else {
//             alert(data['payload']['message'])
//           }
//         }
//       })
//
//     })
//   })
// }

var update_contacts = function(contacts) {

  for (var i = 0; i < contacts.length; i++) {
    $('.contacts').append('<div class="contact" >' + contacts[i] + '</div>')
  }

}

var show_conversation = function(messages) {
  $('.messages').html('')

  var privKeyObj = openpgp.key.readArmored(localStorage.getItem('privkey')).keys[0]

  for (var i = 0; i < messages.length; i++) {
    if (messages[i][2] == Cookies.get('username')) {
      options = {
        message: openpgp.message.readArmored(messages[i][3]),
        privateKey: privKeyObj
      }
      openpgp.decrypt(options).then(function(plaintext) {
        $('.messages').append('<span class="sent_msg" >' + plaintext.data + '</span>')
      })
    } else {
      options = {
        message: openpgp.message.readArmored(messages[i][3]),
        privateKey: privKeyObj
      }
      openpgp.decrypt(options).then(function(plaintext) {
        $('.messages').append('<span class="received_msg" >' + plaintext.data + '</span>')
      })
    }
  }
}
