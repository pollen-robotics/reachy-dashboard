import os
import json

from flask import Flask, request, redirect, url_for, render_template, Response

import tools

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)

notifications = []


@app.route('/update-wifi', methods=['POST'])
def update_wifi():
    tools.setup_new_wifi(request.form['ssid'], request.form['password'])
    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi')
def wifi():
    wlan_config = tools.get_wlan_status()

    status = {}

    if wlan_config['mode'] == 'DHCP':
        status['level'] = 'success'
        status['icon'] = 'wifi'
        status['title'] = 'WiFi'
        status['message'] = 'Connected'

    else:
        status['level'] = 'warning'
        status['icon'] = 'wifi_tethering'
        status['title'] = 'Hotspot'
        status['warning'] = True
        status['message'] = 'No WiFi found...'

    status['SSID'] = wlan_config['SSID']

    return render_template(
        'wifi.html',
        notifications=notifications,
        status=status,
        ip=tools.get_ip(),
        available_networks=tools.get_available_wifis(),
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

@app.route('/api/hotspot', methods=['POST'])
def toggle_hotspot():
    tools.set_hotspot_state(state=request.data.decode())
    return redirect(url_for('wifi'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3972, debug=True)
