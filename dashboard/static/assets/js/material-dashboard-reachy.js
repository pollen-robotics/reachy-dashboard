function updateAvailableFans() {
    const request = new XMLHttpRequest();
    request.responseType = "json";

    let fanSelecter = document.getElementById('fanSelecter');

    while (fanSelecter.options.length > 0) {
      fanSelecter.remove(0);
    }

    request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      for (const [key, value] of Object.entries(this.response)){
        var fanOption = document.createElement("option");
        fanOption.text = key;
        fanSelecter.add(fanOption);
      }
    }
    }
    request.open("GET", "/api/get-fans-info");
    request.send();
}

function switchFanState() {
    let checkboxFan = document.getElementById('fanStateSwitch');
    let fanSelecter = document.getElementById('fanSelecter');

    let selectedFan = fanSelecter.options[fanSelecter.selectedIndex].value;

    const request = new XMLHttpRequest();

    let state = '';
    if (checkboxFan.checked) {
        state = 'on';
    } else {
        state = 'off';
    }
    checkboxFan.disabled = true;
    setTimeout(function(){checkboxFan.disabled = false;}, 1000);
    request.open('GET', '/api/set-fans-state?fan=' + selectedFan + '&state=' + state, true);
    request.send();
}

function changeCompliance(compliance) {
    let partSelecter = document.getElementById('partSelecter');
    let selectedPart = partSelecter.options[partSelecter.selectedIndex].value;

    const request = new XMLHttpRequest();

    request.open('GET', '/api/change-compliance?part=' + selectedPart + '&compliance=' + compliance, true);
    request.send();  
}