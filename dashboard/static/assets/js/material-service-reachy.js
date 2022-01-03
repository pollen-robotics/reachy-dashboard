const makeOneServiceCard = (service) => {
    displayer = document.getElementById("displayerServiceCards");

    const card = document.createElement("div");
    card.className = "card col-sm-4 my-3";

    const cardHeader = document.createElement("h5");
    cardHeader.className = "card-header text-center";
    cardHeader.innerHTML = service;

    const cardBody = document.createElement("div");
    cardBody.className = "card-body text-center";

    const restartButton = document.createElement("button");
    restartButton.className = "btn bg-pollen-dark-blue btn-md mt-1";
    restartButton.id = service+"_restartButton";
    restartButton.innerHTML = "Restart";
    restartButton.onclick = () => restartService(service);

    const stopButton = document.createElement("button");
    stopButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    restartButton.id = "stopButton";
    stopButton.innerHTML = "Stop";
    stopButton.onclick = () => stopService(service);

    cardBody.appendChild(restartButton);
    cardBody.appendChild(stopButton);

    card.appendChild(cardHeader);
    card.appendChild(cardBody);

    displayer.appendChild(card);
}

makeAllServiceCards = () => {
    const request = new XMLHttpRequest();
    request.onload = e => {
      const serviceList = JSON.parse(request.response);
      for (var i = 0; i < serviceList.length; i++) {
          makeOneServiceCard(serviceList[i]);
      }
    }
    request.open("GET", "/api/list_services");
    request.send();
}

stopService = (service) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/stop_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
}

restartService = (service) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/restart_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
}