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
    if net_tools.get_connection_status()['mode'] == 'Hotspot':
        net_tools.set_hotspot_state('off')

    net_tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return redirect(url_for('wifi'))


@app.route('/wifi')
def wifi():
    global wifi_list
    if not net_tools.get_connection_status()['mode'] == 'Hotspot':
        wifi_list = net_tools.get_available_wifis()
    return render_template(
        'wifi.html',
        wifi_list=wifi_list,
    )


@app.route('/halt')
def halt():
    net_tools.halt(delay=5)
    return render_template('halt.html')


@app.route('/api/reachy-status')
def update_status():
    return Response(
        response=json.dumps(net_tools.get_reachy_status()),
        mimetype='application/json',
    )


@app.route('/api/ip')
def update_ip():
    ip = net_tools.get_ip()
    net_tools.display_ip(ip)
    return Response(
        response=json.dumps(ip),
        mimetype='application/json',
    )


@app.route('/api/connection_status')
def update_connection_status():
    return Response(
        response=json.dumps(net_tools.get_connection_status()),
        mimetype='application/json',
    )


@app.route('/api/hotspot', methods=['POST'])
def toggle_hotspot():
    net_tools.set_hotspot_state(state=request.data.decode())
    if request.data.decode() == 'off' and net_tools.get_connection_status()['mode'] == 'None':
        net_tools.set_hotspot_state('on')
    return Response(status=200)


@app.route('/api/available_networks')
def update_available_networks():
    if net_tools.get_connection_status()['mode'] == 'Hotspot':
        global wifi_list
        available_networks = wifi_list
    else:
        available_networks = net_tools.get_available_wifis()
    return Response(
        response=json.dumps(available_networks),
        mimetype='application/json',
    )


@app.route('/api/connection_card_info')
def update_connection_card_info():
    return Response(
        response=json.dumps(net_tools.get_connection_card_info()),
        mimetype='application/json',
    )


if __name__ == '__main__':
    net_tools = tools.NetworkTools()

    net_tools.set_hotspot_state('off')
    wifi_list = net_tools.get_available_wifis()
    net_tools.set_hotspot_state('on')

    net_tools.display_ip(net_tools.get_ip())
    app.run(host='0.0.0.0', port=3972, debug=True)
