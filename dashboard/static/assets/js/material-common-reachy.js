const shutdown =  () => {
    alert("Reachy will power off in one minute.");

    const request = new XMLHttpRequest();
    request.open("GET", "/api/shutdown");
    request.send();
}

getRobotConfig = () => {
    const footer = document.getElementById("footer-container");
    const request = new XMLHttpRequest();
  
    request.onload = e => {
        const config = JSON.parse(request.response);
        footer.innerHTML = `Reachy configuration: ${config['model']} <br />`;
        footer.innerHTML += `Reachy serial number: ${config['serial_number']}`;
    }
    request.open("GET", "/api/get-reachy-info", true);
    request.send();
  }