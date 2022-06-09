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

function handleComplianceClick(compliance) {
  changeCompliance(compliance);
  let onButton = document.getElementById('on-button');
  let offButton = document.getElementById('off-button');
  let smoothButton = document.getElementById('smooth-button');

  onButton.disabled = true;
  offButton.disabled = true;
  smoothButton.disabled = true;

  function activateButtons() {
    onButton.disabled = false;
    offButton.disabled = false;
    smoothButton.disabled = false;
  }

  setTimeout(activateButtons, 1000);
}

function fillPartSelecter() {
    let partSelecter = document.getElementById('partSelecter');

    const request = new XMLHttpRequest();
    request.responseType = "json";

    while (partSelecter.options.length > 0) {
      partSelecter.remove(0);
    }

    request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      for (const [key, value] of Object.entries(this.response)){
        var partOption = document.createElement("option");
        partOption.text = value;
        partSelecter.add(partOption);
      }
    }
    }
    request.open("GET", "/api/get-compliance-config");
    request.send();  
}

function createStateCards() {
  let cardHolder = document.getElementById("jointCardsHolder");

  const request = new XMLHttpRequest();
  request.responseType = "json";

  request.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    for (const [key, value] of Object.entries(this.response)){
      card = createStateCard(key, value);
      cardHolder.appendChild(card);
    }
  }
  }
  request.open("GET", "/api/get-states");
  request.send();
}

function createStateCard(part, jointsState) {
  let col = document.createElement("div");
  col.className = "col-sm";

  let card = document.createElement("div");
  card.className = "card text-center";

  let cardHeader = document.createElement("div");
  cardHeader.className = "card-header";
  cardHeader.innerHTML = part;

  let cardBody = document.createElement("div");
  cardBody.className = "card-body";
  cardBody.id = `${part}-card-body`;

  card.appendChild(cardHeader);
  card.appendChild(cardBody);
  col.appendChild(card);
  return col
}

function fillStatesTables() {
  const request = new XMLHttpRequest();
  request.responseType = "json";

  request.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    for (const [key, value] of Object.entries(this.response)){
      fillStateTable(key, value);
      }
    }
  }
  request.open("GET", "/api/get-states");
  request.send();
}

function fillStateTable(part, jointsState) {
  let cardBody = document.getElementById(`${part}-card-body`);
  while (cardBody.firstChild) {
    cardBody.removeChild(cardBody.lastChild);
  }
  let table = document.createElement("table");
  table.style = "width:100%";

  let row = document.createElement("tr");
  let th = document.createElement("th");
  let thP = document.createElement("th");
  let thT = document.createElement("th");

  thP.innerHTML = "Position";
  thT.innerHTML = "Temperature";

  row.appendChild(th);
  row.appendChild(thP);
  row.appendChild(thT);
  table.appendChild(row);

  for (const [jointName, state] of Object.entries(jointsState)) {
    let row = document.createElement("tr");
    let jn = document.createElement("td");
    let pos = document.createElement("td");
    let temp = document.createElement("td");

    jn.innerHTML = jointName;
    pos.innerHTML = state['position'];

    temp.innerHTML = state['temperature'];

    if (parseFloat(state['temperature']) < 46.0) {
      temp.style.color = "#00AA00";
    } else {
      temp.style.color = "#C14949";
    }

    row.appendChild(jn);
    row.appendChild(pos);
    row.appendChild(temp);
    table.appendChild(row);
  }
  cardBody.appendChild(table);
}