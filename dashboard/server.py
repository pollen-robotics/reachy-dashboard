"""Flask server for RAP-2021."""
import os
import json
import time

from flask import Flask, request, redirect, url_for, render_template, Response

import tools

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)


@app.route('/update-wifi', methods=['POST'])
def update_wifi():
    if tools.get_connection_status()['mode'] == 'Hotspot':
        tools.set_hotspot_state('off')
        time.sleep(4.0)
    tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return redirect(url_for('wifi'))


@app.route('/wifi')
def wifi():
    global wifi_list
    print(wifi_list)
    if not tools.get_connection_status()['mode'] == 'Hotspot':
        # global wifi_list
        wifi_list = tools.get_available_wifis()

    return render_template(
        'wifi.html',
        wifi_list=wifi_list,
    )


@app.route('/halt')
def halt():
    tools.halt(delay=5)
    return render_template('halt.html')


@app.route('/api/reachy-status')
def update_status():
    return Response(
        response=json.dumps(tools.get_reachy_status()),
        mimetype='application/json',
    )


@app.route('/api/ip')
def update_ip():
    ip = tools.get_ip()
    ip_display.display_ip(ip)
    return Response(
        response=json.dumps(ip),
        mimetype='application/json',
    )


@app.route('/api/connection_status')
def update_connection_status():
    return Response(
        response=json.dumps(tools.get_connection_status()),
        mimetype='application/json',
    )


@app.route('/api/hotspot', methods=['POST'])
def toggle_hotspot():
    tools.set_hotspot_state(state=request.data.decode())
    return Response(status=200)


@app.route('/api/available_networks')
def update_available_networks():
    if tools.get_connection_status()['mode'] == 'Hotspot':
        global wifi_list
        available_networks = wifi_list
    else:
        available_networks = tools.get_available_wifis()
    return Response(
        response=json.dumps(available_networks),
        mimetype='application/json',
    )


@app.route('/api/connection_card_info')
def update_connection_card_info():
    return Response(
        response=json.dumps(tools.get_connection_card_info()),
        mimetype='application/json',
    )


if __name__ == '__main__':
    tools.set_hotspot_state('off')
    time.sleep(4.0)
    wifi_list = tools.get_available_wifis()
    print(wifi_list)
    tools.set_hotspot_state('on')
    time.sleep(4.0)
    ip_display = tools.IpDisplay()
    ip_display.display_ip(tools.get_ip())
    app.run(host='0.0.0.0', port=3972, debug=True)
