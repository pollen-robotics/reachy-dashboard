const shutdown =  () => {
    alert("Reachy will power off in one minute.");

    const request = new XMLHttpRequest();
    request.open("GET", "/api/shutdown");
    request.send();
}
