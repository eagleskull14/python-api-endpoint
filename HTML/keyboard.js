var address = "";
var gamemode = false;

document.getElementById("settings").onclick = function () {
    document.getElementById("settingdialog").showModal();
};

document.getElementById("reset").onclick = function () {
    if (address == "") {
        console.log("No Address");
        return;
    }
    sendKeyboard(address + "/keyboard/hold?reset=True");
};

document.getElementById("settingForm").onsubmit = function (event) {
    address = document.getElementById("location").value;
    gamemode = document.getElementById("gamemode").checked;
};

function sendKeyboard(add) {
    try {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", add, false);
        xmlHttp.send(null);
        return xmlHttp.responseText;
    } catch (error) {
        return "no response";
    }
}

function getKeyValue(text) {
    if (text == "⌫") return "backspace";
    if (text == "`") return "backtick";
    if (text == "-") return "minus";
    if (text == "=") return "equal";
    if (text == "[") return "leftbracket";
    if (text == "]") return "rightbracket";
    if (text == "\\") return "backslash";
    if (text == ";") return "semicolon";
    if (text == "'") return "quote";
    if (text == ",") return "comma";
    if (text == ".") return "period";
    if (text == "/") return "slash";
    if (text == "caps") return "capslock";
    if (text == "shift") return "shift";
    if (text == "ctrl") return "ctrl";
    if (text == "alt") return "alt";
    if (text == "caps") return "capslock";
    if (text == "meta") return "meta";
    const arrowMap = {
        "←": "left",
        "→": "right",
        "↑": "up",
        "↓": "down",
    };
    return arrowMap[text] || text.toLowerCase();
}

function handleKeyDown(key) {
    if (address == "") {
        return "No Address";
    }
    if (gamemode) {
        return sendKeyboard(
            address + "/keyboard/hold?id=" + key + "&game=True"
        );
    }
    return sendKeyboard(address + "/keyboard/hold?id=" + key);
}

function handleKeyUp(key) {
    if (address == "") {
        return "No Address";
    }
    if (gamemode) {
        return sendKeyboard(
            address + "/keyboard/hold?id=" + key + "&game=True"
        );
    }
    return sendKeyboard(address + "/keyboard/hold?id=" + key);
}

// Add event listeners to all keys
document.querySelectorAll(".key").forEach(function (keyElement) {
    keyElement.addEventListener("mousedown", function (event) {
        event.preventDefault();
        const key = getKeyValue(this.innerText);
        console.log(handleKeyDown(key));
    });
    keyElement.addEventListener("mouseup", function (event) {
        event.preventDefault();
        const key = getKeyValue(this.innerText);
        console.log(handleKeyUp(key));
    });
    keyElement.addEventListener("touchstart", function (event) {
        event.preventDefault();
        const key = getKeyValue(this.innerText);
        console.log(handleKeyDown(key));
    });
    keyElement.addEventListener("touchend", function (event) {
        event.preventDefault();
        const key = getKeyValue(this.innerText);
        console.log(handleKeyUp(key));
    });
});
