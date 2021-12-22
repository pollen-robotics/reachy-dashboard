const makeAllCards = () => {
  const request = new XMLHttpRequest();
  request.onload = e => {
    const status = JSON.parse(request.response);

    fillStatsCard(status);

    for (const part in status) {
      const partsElement = document.getElementById("reachyParts");
      partsElement.appendChild(makeCardForPart(part, status[part]));
    }
  }
  request.open("GET", "/api/missing_modules_names");
  request.send();
}

const makeCardForPart = (part, missing_modules) => {
  const iconName = {"ok": "check_circle", "problem": "highlight_off"};
  const headerLevel = {"ok": "success", "problem": "danger"};

  const card = document.createElement("div"); 
  card.className = "card card-stats";

  const cardHeader = document.createElement("div");

  const cardIcon = document.createElement("div");
  cardIcon.className = "card-icon";
  const materialIcon = document.createElement("i");
  materialIcon.className = "material-icons";
  cardIcon.appendChild(materialIcon);

  const cardCategory = document.createElement("p");
  cardCategory.className = "card-category";
  cardCategory.innerHTML = prettyName(part);

  const cardTitle = document.createElement("h3");
  cardTitle.className = "card-title"

  if (missing_modules.length == 0) {
    materialIcon.innerHTML = iconName["ok"];
    cardHeader.className = `card-header card-header-${headerLevel["ok"]} card-header-icon`;
    cardTitle.innerHTML = "";
  }
  else {
    materialIcon.innerHTML = iconName["problem"];
    cardHeader.className = `card-header card-header-${headerLevel["problem"]} card-header-icon`;
    cardTitle.innerHTML = "Missing modules";
  }

  cardHeader.appendChild(cardIcon);
  cardHeader.appendChild(cardCategory);
  cardHeader.appendChild(cardTitle);

  card.appendChild(cardHeader);  

  const cardFooter = document.createElement("div");
  cardFooter.className = "card-footer";
  const stats = document.createElement("div");
  stats.className = "stats";

  centerText = document.createElement("center");
  cardText = document.createElement("p");
  cardText.className = "card-text";
  
  card.appendChild(centerText);
  centerText.appendChild(cardText);

  if (missing_modules.length != 0) {
    cardText.innerHTML = prettyContainerList(missing_modules);
  }
  else {
    cardText.innerHTML = `Reachy's ${part} looks good!`;
  }

  cardFooter.appendChild(stats);
  card.appendChild(cardFooter);

  const wrapper = document.createElement("div");
  wrapper.className = "col-md-4";
  wrapper.appendChild(card);

  return wrapper;
};

const prettyContainerList = (list) => {
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

  for (var i = 0; i < missing_modules.length; i++) {
    if (missing_modules[i] == 'l_force_gripper' || missing_modules[i] == 'r_force_gripper'){
      var missing_force_sensor = true;
    }
  }
  if (missing_modules.length == 1) {
    if (missing_force_sensor == true) {
      writeMissingForceFooter();
    }
    else {writeMissingMotorFooter()};
  }
  else {
    writeMissingMotorFooter();
    if (missing_force_sensor == true) {
      writeMissingForceFooter();
    } 
  }
}

const writeMissingMotorFooter = () => {
  card = document.getElementById("statsCard");

  txtPreLinkMotor = document.createElement("a");
  txtPreLinkMotor.innerHTML = "Check Reachy's 2021 documentation to learn how to &nbsp";
  txtLinkMotor = document.createElement("a");
  txtLinkMotor.href = "https://docs.pollen-robotics.com/help/system/reconnect-motor/"
  txtLinkMotor.target = "_blank";
  txtLinkMotor.innerHTML = "reconnect a motor. <br/>"

  card.appendChild(txtPreLinkMotor);
  card.appendChild(txtLinkMotor);
}

const writeMissingForceFooter = () => {
  card = document.getElementById("statsCard");

  txtPreLinkForce = document.createElement("a");
  txtPreLinkForce.innerHTML = "Check Reachy's 2021 documentation to learn how to &nbsp";
  txtLinkForce = document.createElement("a");
  txtLinkForce.href = "https://docs.pollen-robotics.com/help/system/reconnect-load-sensor/"
  txtLinkForce.target = "_blank";
  txtLinkForce.innerHTML = "reconnect a force sensor. <br/>"

  card.appendChild(txtPreLinkForce);
  card.appendChild(txtLinkForce);
}

const fillStatsCard = (status) => {
  statsCard = document.getElementById("statsCard");
  all_parts = [];

  for (part in status) {
    all_parts = all_parts.concat(status[part]);
  }
  if (all_parts.length == 0){
    statsCard.hidden = true;
  }
  else {
    counter_force_sensors = 0;
    counter_motors = 0;
    for (var i = 0; i < all_parts.length; i++) {
      if (all_parts[i] == 'r_force_gripper' || all_parts[i] == 'l_force_gripper'){
        counter_force_sensors += 1;
      }
      else {
        counter_motors += 1;
      }
    }
    if (counter_motors != 0){
      writeMissingMotorFooter();
    }
    if (counter_force_sensors != 0){
      writeMissingForceFooter();
    }
  }
}

const alertIfNoModules = () => {
  const request = new XMLHttpRequest();
  request.onload = e => {
    const missing_modules_bool = JSON.parse(request.response);
    if (missing_modules_bool == "all_missing") {
      alert("Each Reachy's module is missing, did you turn the switch in Reachy's back before turning on its computer?");
    }
  }
  request.open("GET", "/api/missing_modules_bool");
  request.send();
}

const refreshStatus = () => {
    makeAllCards();
    alertIfNoModules();
};
