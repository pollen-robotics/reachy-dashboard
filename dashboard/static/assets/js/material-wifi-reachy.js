function displayIp() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById('ipAddress').innerHTML = this.response.slice(1,-1);
      }
    }
    request.open("GET", "/api/ip");
    request.send();
}

function handleOnloadHotspot() {
    checkboxHotspot = document.getElementById('hotspotSwitch');
    const request = new XMLHttpRequest();
    request.responseType = "json";

    request.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        if (this.response['mode'] == 'Hotspot') {
          checkboxHotspot.checked = true;
        }
        else {
          checkboxHotspot.unchecked = true;
        }
      }
    }
    request.open("GET", "/api/connection_status");
    request.send();
}

function fillConnectionCard() {
    var cardTitle = document.getElementById("conCardTitle");
    var cardSSID = document.getElementById("conCardSSID");
    var cardMessage = document.getElementById("conCardMsg");

    const request = new XMLHttpRequest();
    request.responseType = "json";

    request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      cardTitle.innerHTML = this.response['title'];
      cardSSID.innerHTML = this.response['SSID'];
      cardMessage.innerHTML = this.response['message'];
      }
    }
    request.open("GET", "/api/connection_card_info");
    request.send();
}

function onloadAvailableNetworks(wifi_list) {
    var ssidSelecter = document.getElementById('ssidSelecter');
    for (let wifiId in wifi_list){
      var wifiOption = document.createElement("option");
      wifiOption.text = wifi_list[wifiId];
      ssidSelecter.add(wifiOption);
      }
}

function revealPassword() {
    var passwordForm = document.getElementById('passwordForm');
    if (passwordForm.type == 'password') {
      passwordForm.type = 'text';
    }
    else {
      passwordForm.type = 'password';
    }
}

function check_if_no_network() {
    checkboxHotspot = document.getElementById('hotspotSwitch');
    const request = new XMLHttpRequest();
    request.responseType = "json";

    request.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) { 
        if (this.response['mode'] == 'None') {
          checkboxHotspot.checked = true;
          switchHotspot();
        }
      }
    }
    request.open("GET", "/api/connection_status");
    request.send();
  }

function switchHotspot() {
    checkboxHotspot = document.getElementById('hotspotSwitch');

    const request = new XMLHttpRequest();
    let state = "";
    if (checkboxHotspot.checked) {
      state = "on";
    } else {
      state = "off";
    }
    checkboxHotspot.disabled = true;
    setTimeout(function(){checkboxHotspot.disabled = false;}, 5000);
    setTimeout(updateEverything, 5000);
    request.open("POST", "/api/hotspot");
    request.send(state);
}

function updateAvailableNetworks() {
    const request = new XMLHttpRequest();
    request.responseType = "json";

    var ssidSelecter = document.getElementById('ssidSelecter');

    while (ssidSelecter.options.length > 0) {
      ssidSelecter.remove(0);
    }

    request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      for (let wifiId in this.response){
        var wifiOption = document.createElement("option");
        wifiOption.text = this.response[wifiId];
        ssidSelecter.add(wifiOption);
      }
    }
    }
    request.open("GET", "/api/available_networks");
    request.send();
}

function displayModalUpdatedWifi() {
    var modalWifi = new bootstrap.Modal(document.getElementById('modalUpdatedWifi'), {})
    modalWifi.show();
}

function updateEverything() {
    fillConnectionCard();
    check_if_no_network();
    updateAvailableNetworks();
    displayIp();
}