let interval = {};

const makeOneAppCard = (app) => {
    displayer = document.getElementById("displayerAppCards");

    const card = document.createElement("div");
    card.className = "card col-sm-4 my-3";

    var cardHeader = document.createElement("h5");
    cardHeader.className = "card-header text-center";
    cardHeader.innerHTML = app;
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("id", "headerSvg_"+app)
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
    restartButton.id = app+"_restartButton";
    restartButton.innerHTML = "Restart";
    restartButton.onclick = () => restartApp(app, restartButton);

    const stopButton = document.createElement("button");
    stopButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    stopButton.id = app+"_stopButton";
    stopButton.innerHTML = "Stop";
    stopButton.onclick = () => stopApp(app, stopButton);

    const logButton = document.createElement("button");
    logButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    logButton.id = app+"_logButton";
    logButton.innerHTML = "Show logs";
    logButton.onclick = () => getAppStatus(app);

    const testButton = document.createElement("button");
    testButton.className = "btn bg-pollen-dark-blue btn-md mt-1 ms-3";
    testButton.id = app+"_testButton";
    testButton.innerHTML = "Test";
    testButton.onclick = () => updateProgressBar();

    const cardFooter = document.createElement("div");
    cardFooter.className = "card-footer text-center";
    const footerText = document.createElement("i");
    footerText.id = "footerStatus-"+app;
    cardFooter.appendChild(footerText);

    cardBody.appendChild(restartButton);
    cardBody.appendChild(stopButton);
    cardBody.appendChild(logButton);

    card.appendChild(cardHeader);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);

    displayer.appendChild(card);
    setFooterStatus(app);
}

makeAllAppCards = () => {
    const request = new XMLHttpRequest();
    request.onload = e => {
      const appList = JSON.parse(request.response);
      for (var i = 0; i < appList.length; i++) {
          makeOneAppCard(appList[i]);
      }
    }
    request.open("GET", "/api/list_apps");
    request.send();
    preventMultipleAppsActive();
}

stopApp = (app, button) => {
    clearLog();
    button.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/stop_app", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(app));
    setTimeout(() => setFooterStatus(app), 2000);
    setTimeout(() => {button.disabled = false; window.location.reload();}, 2000);
}

restartApp = (app, button) => {
    updateProgressBar(app)
    clearLog();
    button.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/restart_app", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(app));
    setTimeout(() => setFooterStatus(app), 10000);
    setTimeout(function(){button.disabled = false;}, 10000);
}

setFooterStatus = (app) => {
    const footer = document.getElementById("footerStatus-"+app);
    const headerSvg = document.getElementById("headerSvg_"+app);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/is_app_running", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = e => {
        const appStatus = JSON.parse(xhr.response);
        footer.innerHTML = appStatus;
        if (appStatus == 'running') {
            headerSvg.setAttribute("fill", "#c14949");
        }
        else {
            headerSvg.setAttribute("fill", "");
        }

      }
    xhr.send(JSON.stringify(app));
}

getAppStatus = (app) => {
    const displayer = document.getElementById("logDisplayer");

    const request = new XMLHttpRequest();
    request.onload = e => {
        displayer.innerHTML = "<pre>" + request.response + "</pre>";
        document.getElementById("clearLogButton").hidden = false;
    }
    request.open("POST", "/api/status_app", true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(app));
}

clearLog = () => {
    const displayer = document.getElementById("logDisplayer");
    displayer.innerHTML = "";
    document.getElementById("clearLogButton").hidden = true;
}

preventMultipleAppsActive = () => {
    const request = new XMLHttpRequest();
    request.onload = e => {
      const appListToDisable = JSON.parse(request.response);
      for (var i = 0; i < appListToDisable.length; i++) {
          document.getElementById(appListToDisable[i]+"_restartButton").disabled = true;
          document.getElementById(appListToDisable[i]+"_stopButton").disabled = true;
      }
    }
    request.open("GET", "/api/app_disable");
    request.send();
}

updateProgressBar = (app) => {
    const progressBar = document.getElementById("appProgressBar");
    const progressBarContainer = document.getElementById("progressBarContainer");

    progressBarContainer.hidden = false;
    document.getElementById("restartAppName").innerHTML = "Restarting " + app + "...";

    let i = 0;
    progressBar.ariaValueNow = i;
    progressBar.innerHTML = `${i}%`;
    progressBar.style = `width: ${i}%`;

    const interval = setInterval(addProgress, 210);
    function addProgress() {
        if (i < 100) {
            i++;
            progressBar.ariaValueNow = i;
            progressBar.innerHTML = `${i}%`;
            progressBar.style = `width: ${i}%`;            
        }
    }
    setTimeout(() => {progressBarContainer.hidden = true; window.location.reload();}, 5000);

}