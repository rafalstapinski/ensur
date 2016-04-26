/*

    Application design happens in design object.
    API calls handled by calls object.
    app object waits for events, runs calls and design, does client side calc

*/

var view = {

    firstLaunch: function() {
        $(".firstLaunch").show();
    },
    normalLaunch: function() {
        $(".normalLaunch").show();
    },
    step1: function() {
        $("#step1").show();
    },
    step2: function() {
        $("#step1").hide();
        $("#step2").show();
    },
    step3: function() {
        $("#step2").hide();
        $("#step3").show();
    },
    new: function() {

    },
    newMessage: function() {

    },
    newContact: function() {

    },
    loading: function() {
        //overlay loading screen, don't go to load.html
        console.log("start loading screen");
    },
    endLoading: function() {
        //delete overlay
        console.log("end loading screen");
    },
    finishSetup: function() {
        //view for after setup

        console.log("finish setup");
    },
    mainScreen: function() {
        //display main screen
        location.href="main.html";
    }

}

var calls = {

    checkUsername: function() {

        var username = $("#username").val();

        $.post({
            url: "http://localhost:8003/user/checkusername",
            data: {
                "username": username
            },
            success: function(data) {
                if (data["status"] == 200) {
                    if (data["payload"]["unique"] == true) {
                        app.step2(username);
                    } else {
                        alert("Username not unique. ");
                    }
                } else {
                    alert(data["payload"]["error"]);
                }
            },
            error: function(e) {
                alert("There was some sort of error. Try again soon. ");
            }
        });
    },
    createUser: function(username, password, pubkey, privkey) {

        $.post({
            url: "http://localhost:8003/user/createuser",
            data: {
                "username": username,
                "password": password,
                "pubkey": pubkey
            },
            success: function(data) {
                if (data["status"] == 200) {
                    view.endLoading();
                    localStorage.setItem("privkey", privkey);
                    localStorage.setItem("username", username);
                    view.finishSetup();
                    app.normalLaunch();
                } else {
                    alert(data["payload"]["error"])
                }
            },
            error: function(e) {
                alert("There was some sort of error. Try again soon. ");
            }
        });
    },
    login: function() {
        var password = $(".normalLaunch input").val();

        console.log(password);

    }
};

var app = {

    initialize: function() {
        this.bindEvents();

    },
    bindEvents: function() {

        document.addEventListener("deviceready", this.onDeviceReady, false);

        this.onDeviceReady();
    },
    onDeviceReady: function() {

        this.receivedEvent("deviceready");
    },
    receivedEvent: function(id) {

        var privkey = localStorage.getItem("privkey");

        if (privkey == null) {
            this.firstLaunch();          // go through first launch sequence
        } else {
            this.normalLaunch();        //go through normal launch sequence
        }

    },
    firstLaunch: function() {
        view.firstLaunch();
        this.step1();
    },
    step1: function() {
        view.step1();
        $("#checkUsername").click(calls.checkUsername);
    },
    step2: function(username) {
        view.step2();

        $("#step2 button").click(function() {

            var password = $("#password").val();

            if (password == $("#passwordAgain").val()) {
                app.step3(username, password);
            } else {
                alert("Passwords don't match. ");
            }

        });
    },
    step3: function(username, password) {

        view.step3();

        $("#generateKeys").click(function() {

            var openpgp = window.openpgp;

            var options = {
                userIds: [{name: username}],
                numBits: 4096,
                passphrase: password
            };

            view.loading();

            openpgp.generateKey(options).then(function(key) {

                var privkey = key.privateKeyArmored;
                var pubkey = key.publicKeyArmored;

                //check cordova network connection here
                //before continuing

                calls.createUser(username, password, pubkey, privkey);

            });
        });
    },
    normalLaunch: function() {

        view.normalLaunch();

        $(".normalLaunch button").click(calls.login);

    },
    mainScreen: function() {

        view.mainScreen();

        $("#new").click(view.new);
        $("#newContact").click(this.newContact);
        $("#newMessage").click(this.newMessage);

    },
    newContact: function() {
        view.newContact();


        this.runHandle();
    },
    newMessage: function() {
        view.newMessage();



        this.runHandle();
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
