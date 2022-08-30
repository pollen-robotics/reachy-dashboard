let interval = {};

const makeOneServiceCard = (service) => {
    displayer = document.getElementById("displayerServiceCards");

    const card = document.createElement("div");
    card.className = "card col-sm-4 my-3";

    var cardHeader = document.createElement("h5");
    cardHeader.className = "card-header text-center";
    cardHeader.innerHTML = service;
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("id", "headerSvg_"+service)
    svg.setAttribute("height",16);
    svg.setAttribute("width",16);
    document.body.appendChild(svg);
    var circles = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circles.setAttribute("cx",10);
    circles.setAttribute("cy",7);
    circles.setAttribute("r",6);
    svg.appendChild(circles);
    cardHeader.appendChild(svg);

    const cardBody = document.createElement("div");
    cardBody.className = "card-body text-center";

    const restartButton = document.createElement("button");
    restartButton.className = "btn bg-pollen-dark-blue btn-md mt-1";
    restartButton.id = service+"_restartButton";
    restartButton.innerHTML = "Restart";
    restartButton.onclick = () => restartService(service, restartButton);

    const stopButton = document.createElement("button");
    stopButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    stopButton.id = service+"_stopButton";
    stopButton.innerHTML = "Stop";
    stopButton.onclick = () => stopService(service, stopButton);

    const logButton = document.createElement("button");
    logButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    logButton.id = service+"_logButton";
    logButton.innerHTML = "Show logs";
    logButton.onclick = () => getServiceStatus(service);

    const testButton = document.createElement("button");
    testButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    testButton.id = service+"_testButton";
    testButton.innerHTML = "Test";
    testButton.onclick = () => updateProgressBar();

    const cardFooter = document.createElement("div");
    cardFooter.className = "card-footer text-center";
    const footerText = document.createElement("i");
    footerText.id = "footerStatus-"+service;
    cardFooter.appendChild(footerText);

    cardBody.appendChild(restartButton);
    cardBody.appendChild(stopButton);
    cardBody.appendChild(logButton);

    card.appendChild(cardHeader);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);

    displayer.appendChild(card);
    setFooterStatus(service);
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

stopService = (service, button) => {
    clearLog();
    button.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/stop_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
    setTimeout(() => setFooterStatus(service), 2000);
    setTimeout(function(){button.disabled = false;}, 2000);
}

restartService = (service, button) => {
    updateProgressBar(service)
    clearLog();
    button.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/restart_service", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(service));
    setTimeout(() => setFooterStatus(service), 10000);
    setTimeout(function(){button.disabled = false;}, 10000);
}

setFooterStatus = (service) => {
    const footer = document.getElementById("footerStatus-"+service);
    const headerSvg = document.getElementById("headerSvg_"+service);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/is_service_running", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = e => {
        const serviceStatus = JSON.parse(xhr.response);
        footer.innerHTML = serviceStatus;
        if (serviceStatus == 'running') {
            headerSvg.setAttribute("fill", "#c14949");
        }
        else {
            headerSvg.setAttribute("fill", "");
        }

      }
    xhr.send(JSON.stringify(service));
}

getServiceStatus = (service) => {
    const displayer = document.getElementById("logDisplayer");

    const request = new XMLHttpRequest();
    request.onload = e => {
        displayer.innerHTML = "<pre>" + request.response + "</pre>";
        document.getElementById("clearLogButton").hidden = false;
    }
    request.open("POST", "/api/status_service", true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(service));
}

clearLog = () => {
    const displayer = document.getElementById("logDisplayer");
    displayer.innerHTML = "";
    document.getElementById("clearLogButton").hidden = true;
}

getRobotConfig = () => {
    const footer = document.getElementById("footer-container");
    const request = new XMLHttpRequest();

    request.onload = e => {
        const config = JSON.parse(request.response);
        footer.innerHTML = `Reachy configuration: ${config}`;
    }
    request.open("GET", "/api/get_reachy_config", true);
    request.send();
}

updateProgressBar = (service) => {
    const progressBar = document.getElementById("serviceProgressBar");
    const progressBarContainer = document.getElementById("progressBarContainer");

    progressBarContainer.hidden = false;
    document.getElementById("restartServiceName").innerHTML = "Restarting " + service + "...";

    let i = 0;
    progressBar.ariaValueNow = i;
    progressBar.innerHTML = `${i}%`;
    progressBar.style = `width: ${i}%`;

    const interval = setInterval(addProgress, 100);
    function addProgress() {
        if (i < 100) {
            i++;
            progressBar.ariaValueNow = i;
            progressBar.innerHTML = `${i}%`;
            progressBar.style = `width: ${i}%`;            
        }
    }
    setTimeout(() => progressBarContainer.hidden = true, 12000);
}