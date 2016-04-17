$(document).ready(function () {

    var openpgp = window.openpgp;

    $("#generate_keys").click(function() {

        var options = {
            userIds: [{ name:'Jon Smith', email:'jon@example.com' }], // multiple user IDs
            numBits: 4096,                                            // RSA key size
            passphrase: 'super long and hard to guess secret'         // protects the private key
        };

        openpgp.generateKey(options).then(function(key) {
            var privkey = key.privateKeyArmored; // '-----BEGIN PGP PRIVATE KEY BLOCK ... '
            var pubkey = key.publicKeyArmored;   // '-----BEGIN PGP PUBLIC KEY BLOCK ... '


            console.log(privkey);
            console.log(pubkey);


            window.privkey = privkey;
            window.pubkey = pubkey;

        });

    });

    $("#encrypt").click(function() {

        var msg = $("#msg").val();

        var msg_buf = str_to_ui(msg);

        options = {
            data: msg,
            publicKeys: openpgp.key.readArmored(pubkey).keys,
            armor: false
        };

        openpgp.encrypt(options).then(function(ciphertext) {
            var encrypted = ciphertext.message.packets.write();
            console.log(encrypted);
            window.dec = encrypted;
        });

    });

    $("#decrypt").click(function() {

        var msg = $("#dec").val();

        console.log(window.dec);

        var encrypteduint8array = new Uint8Array(window.dec);

        console.log(encrypteduint8array);

        options = {
            message: openpgp.message.read(encrypteduint8array),
            privateKey: openpgp.key.readArmored(privkey).keys[0],
            format: "utf8"
        };

        openpgp.decrypt(options).then(function(plaintext) {
            console.log(plaintext.data);
        });


    });

});


function ui_to_str(buf) {

    return String.fromCharCode.apply(null, new Uint8Array(buf));

}

function str_to_ui(str) {

    var buf = new ArrayBuffer(str.length*2);
    var buf_view = new Uint8Array(buf);

    for (var i = 0, len = str.length; i < len; i++) {

        buf_view[i] = str.charCodeAt(i);

    }

    return buf;

}
