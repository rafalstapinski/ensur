// check to see functions are actually returning and its not just running function inside function because that would suck, i think

var calls = { //check for online before call
    createUser: function() {
        $.ajax({
            url: "http://localhost:8000/user/new",
            data: {
                "username": sessionStorage.getItem("username"),
                "pubkey": sessionStorage.getItem("pubkey")
            },
            success: function(data) {
                if (data["status"] == 200) {
                    app.step4();
                } else {
                    views.alert(data["payload"]["error"]);
                }
            }
        });
    },
    checkUsername: function() {
        console.log($("#usernameInput").val());
        $.ajax({
            url: "http://localhost:8000/user/exists",
            data: {
                "username": $("#usernameInput").val()
            },
            success: function(data) {
                if (data["status"] == 200) {
                    sessionStorage.setItem("username", data["payload"]["username"]);
                    app.step2();
                } else {
                    views.alert(data["payload"]["error"]);
                }
            }
        });
    }
}

var views = { //holla
    tooGood: function() {
        return true;
    },
    step1: function() {
        $(".step1").show();
    },
    step2: function() {
        $(".step1").hide();
        $(".step2").show();
    },
    step3: function() {
        $(".step2").hide();
        $(".step3").show();
    },
    step4: function() {
        $(".step3").hide();
        $(".step4").show();
    },
    alert: function(msg) {
        alert(msg); //change this later
    },
    showLoading: function() {
        console.log("show loading");
        $(".loading").show();
    },
    hideLoading: function() {
        console.log("hide loading");
        $(".loading").hide();
    }
}

var app = {

    initialize: function() {
        this.bindEvents();
    },
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
        document.addEventListener("online", this.onOnline, false);
        document.addEventListener("offline", this.onOffline, false);
        app.onOnline();
        app.onDeviceReady();
    },
    onDeviceReady: function() {
        var firstLaunch = localStorage.getItem("setup");
        if (firstLaunch == "true") {
            app.normalLaunch();
        } else {
            app.step1();
        }
    },
    normalLaunch: function() {
        alert("normal launch");
    },
    step1: function() {
        views.step1();
        $("#checkUsername").click(calls.checkUsername);
    },
    step2: function() {
        views.step2();
        $("#generateKeys").click(function() {
            views.showLoading();

            var options = {
                userIds: [{ name: sessionStorage.getItem("username") }],
                numBits: 4096,
                passphrase: 'super long and hard to guess secret' //change to user defined
            };

            openpgp.generateKey(options).then(function(key) {
                var privkey = key.privateKeyArmored;
                var pubkey = key.publicKeyArmored;
                sessionStorage.setItem("privkey", privkey);
                sessionStorage.setItem("pubkey", pubkey);
                console.log(sessionStorage.getItem("privkey"));
                console.log(sessionStorage.getItem("pubkey"));
                views.hideLoading();
                app.step3();
            });
        });
    },
    step3: function() {
        views.step3();
        $("#createUser").click(calls.createUser);
    },
    step4: function() {
        views.step4();
        $("#finishSetup").click(app.finishSetup);
    },
    finishSetup: function() {
        localStorage.setItem("setup", true);
        app.normalLaunch();
    },
    normalLaunch: function() {
        alert("normal launch now");
    },
    onOnline: function() {
        sessionStorage.setItem("online", true);
    },
    onOffline: function() {
        sessionStorage.setItem("online", false);
    },
    isOnline: function() {
        if (sessionStorage.getItem("online")) {
            return true;
        } return false;
    }
};

app.initialize();
