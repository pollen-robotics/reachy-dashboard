const makeAllCards = () => {
  const request = new XMLHttpRequest();
  request.onload = e => {
    const status = JSON.parse(request.response);

    for (const part in status) {
      const partsElement = document.getElementById("reachyPartCards");
      partsElement.appendChild(makeCardForPart(part, status[part]));
    }
  }
  request.open("GET", "/api/missing_modules_names");
  request.send();
}

const makeCardForPart = (part, missing_modules) => {
  const card = document.createElement("div");
  card.className = "card text-center";

  const cardHeader = document.createElement("h5");
  cardHeader.className = "card-header";
  cardHeader.innerHTML = prettyName(part);

  const cardBody = document.createElement("div");
  cardBody.className = "card-body";

  if (missing_modules.length == 0) {
    cardBody.innerHTML = `Reachy's ${part} looks good!`;
  }
  
  else {
    const cardTitle = document.createElement("h5");
    cardTitle.innerHTML = "Missing modules";

    const modulesList = document.createElement("div");
    modulesList.innerHTML = prettyModuleList(missing_modules); 

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(modulesList);

    writeStatMsg(missing_modules);
  }

  card.appendChild(cardHeader);
  card.appendChild(cardBody);

  const wrapper = document.createElement("div");
  wrapper.className = "col-sm-4 my-1";
  wrapper.appendChild(card);

  return wrapper;
}

const prettyModuleList = (list) => {
  var pretty = "";
  for (var i = 0; i < list.length; i++) {
    pretty = pretty.concat(list[i] + "<br />");
  }
  return pretty;
}
const prettyName = (str) => {
  const splitStr = str.toLowerCase().split('_');
  for (var i = 0; i < splitStr.length; i++) {
      splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
  }
  return splitStr.join(' '); 
}

const writeStatMsg = (missing_modules) => {
  const statsTxt = document.createElement("a");
  var missing_force_sensor = false;
  var missing_motor = false;
  for (var i = 0; i < missing_modules.length; i++) {
    if (missing_modules[i] == 'l_force_gripper' || missing_modules[i] == 'r_force_gripper'){
      var missing_force_sensor = true;
    }
  }
  if (missing_modules.length == 1) {
    if (missing_force_sensor == false) {
      missing_motor = true;
    }
  }
  else {
    missing_motor = true;
  }
  displayInfo(missing_motor, missing_force_sensor);
}

const alertIfNoModules = () => {
  const request = new XMLHttpRequest();
  request.onload = e => {
    const missing_modules_bool = JSON.parse(request.response);
    if (missing_modules_bool == "all_missing") {
      var modalWifi = new bootstrap.Modal(document.getElementById('modalNoModules'), {})
      modalWifi.show();
    }
  }
  request.open("GET", "/api/missing_modules_bool");
  request.send();
}

const displayInfo = (motors, sensor) => {
  alertMotor = document.getElementById('alertNoMotor');
  alertSensor = document.getElementById('alertNoSensor');
  alertAll = document.getElementById('alertAllMissing');

  alertDisplayer = document.getElementById('alertDisplayer');
  allMissingAlertRow = document.getElementById('allMissingAlertRow');

  if (motors == true) {
    alertDisplayer.appendChild(alertMotor);
  }
  if (sensor == true) {
    alertDisplayer.appendChild(alertSensor);
  }
  if (motors == true && sensor == true) {
    allMissingAlertRow.appendChild(alertAll);
  }
}

const hideConnectionButton = () => {
  const request = new XMLHttpRequest();
  request.onload = e => {
    const missing_modules_bool = JSON.parse(request.response);
    if (missing_modules_bool == "none_missing") {
      document.getElementById("containerConnectButton").hidden = false;
    }
  }
  request.open("GET", "/api/missing_modules_bool");
  request.send();
}

const refreshStatus = () => {
  alertIfNoModules();
  makeAllCards();
  hideConnectionButton();
}
