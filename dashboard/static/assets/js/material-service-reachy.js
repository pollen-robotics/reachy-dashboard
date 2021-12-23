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
    restartButton.id = "restartButton";
    restartButton.innerHTML = "Restart";
    // restartButton.onclick = function(){console.log('Wesh')};
    // restartButton.addEventListener("click", console.log('Restart'));
    restartButton.onclick = restartService(service);

    const stopButton = document.createElement("button");
    stopButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    stopButton.innerHTML = "Stop";
    stopButton.onclick = stopService(service);

    // stopButton.onclick = 'console.log("Stop")';
    // stopButton.addEventListener("click", console.log('Stop'));

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
    const request = new XMLHttpRequest();
    request.open("POST", "/api/stop_service");
    request.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
    };
    request.send(service);
    }
}

restartService = (service) => {
    const request = new XMLHttpRequest();
    request.open("POST", "/api/restart_service");
    console.log('yp');
    request.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
    };
    request.send('reachy_sdk_server.service');
    console.log('restart');
    }
}