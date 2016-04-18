var calls = {

    checkUsername: function() {

        $.post({
            url: "http://localhost:8003",
            data: $("#username").val(),
            success: function(data) {
                if (data["status"] == 200) {
                    if (data["payload"]["unique"] == true) {
                        app.step2();
                    } else {
                        alert("Username not unique. ");
                    }
                } else {
                    data["payload"]["error"];
                }
            },
            error: function(e) {
                alert("There was some sort of error. Try again soon. ");
            }
        });
    }

};

var app = {

    initialize: function() {
        this.bindEvents();

    },
    bindEvents: function() {

        $("#checkUsername").on("click", calls.checkUsername);

        document.addEventListener("deviceready", this.onDeviceReady, false);

        this.onDeviceReady();
    },
    onDeviceReady: function() {

        this.receivedEvent("deviceready");
    },
    receivedEvent: function(id) {

        var storage = window.localStorage;

        var setup = storage.getItem("setup");

        if (setup == null) {
            this.firstLaunch();                 // go through first launch sequence
        } else {
            $(".normalLaunch").show();          //go through normal launch sequence
        }

    },
    firstLaunch: function() {
        $(".firstLaunch").show();
        this.step1();
    },
    step1: function() {
        $("#step1").show();
    },
    step2: function() {
        $("#step1").hide();
        $("#step2").show();
    }
};

app.initialize();





/*$(document).ready(function () {

    var openpgp = window.openpgp;


    $("#generate_keys").click(function() {

        var options = {
            userIds: [{ name:'Jon Smith', email:'jon@example.com' }], // multiple user IDs
            numBits: 4096,                                            // RSA key size
            passphrase: 'super long and hard to guess secret'         // protects the private key
        };

        openpgp.generateKey(options).then(function(key) {
            window.privkey = key.privateKeyArmored; // '-----BEGIN PGP PRIVATE KEY BLOCK ... '
            window.pubkey = key.publicKeyArmored;   // '-----BEGIN PGP PUBLIC KEY BLOCK ... '


            console.log(window.privkey);
            console.log(window.pubkey);

        });

    });

    $("#encrypt").click(function() {

        var msg = $("#msg").val();

        var msg_buf = str_to_ui(msg);

        options = {
            data: msg,
            publicKeys: openpgp.key.readArmored(window.pubkey).keys,
            armor: false
        };

        openpgp.encrypt(options).then(function(ciphertext) {
            window.encrypted = ciphertext.message.packets.write();
            console.log(window.encrypted);
        });

    });

    $("#decrypt").click(function() {

        options = {
            message: openpgp.message.read(window.encrypted),
            privateKey: openpgp.key.readArmored(window.privkey).keys[0],
            format: "binary"
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


*/
