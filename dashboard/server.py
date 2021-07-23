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
    print(tools.get_connection_status()['mode'])
    if tools.get_connection_status()['mode'] == 'Hotspot':
        tools.set_hotspot_state('off')
        time.sleep(4.0)
        print(tools.get_available_wifis())
    tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi')
def wifi():
    tools.set_hotspot_state('off')
    time.sleep(2.0)
    first_wifi_list = tools.get_available_wifis()
    if not tools.get_connection_status()['mode'] == 'Wifi':
        tools.set_hotspot_state('on')
    return render_template(
        'wifi.html',
        first_wifi_list=first_wifi_list,
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
    return Response(
        response=json.dumps(tools.get_ip()),
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
    return Response(
        response=json.dumps(tools.get_available_wifis()),
        mimetype='application/json',
    )


@app.route('/api/connection_card_info')
def update_connection_card_info():
    return Response(
        response=json.dumps(tools.get_connection_card_info()),
        mimetype='application/json',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3972, debug=True)
