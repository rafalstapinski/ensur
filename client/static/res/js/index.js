var set_keys = function(username, passphrase) {



  var options = {
    userIds: [{name: username}],
    passphrase: passphrase
  }

  openpgp.generateKey(options).then(function(key) {
    var privkey = key.privateKeyArmored
    var pubkey = key.publicKeyArmored

    $('.loading_screen').hide()

    $.ajax({
      type: 'post',
      data: {
        pubkey: pubkey,
        username: username,
      },
      url: 'http://localhost:8080/user/new',
      success: function(data) {
        if (data.status == 200) {
          Cookies.set('username', username)
          window.localStorage.setItem('pubkey', pubkey)
          window.localStorage.setItem('privkey', privkey)
          location.href='messages'
        }
      }
    })
  })
}

var randomString = function(length) {
  var text = ''
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  for(var i = 0; i < length; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length))
  }
  return text
}
