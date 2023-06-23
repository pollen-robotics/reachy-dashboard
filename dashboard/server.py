"""Flask server for RAP-2021."""
import os
import json

from flask import Flask, request, redirect, url_for, render_template, Response, jsonify

from reachy_utils.config import get_reachy_model, get_reachy_generation, get_reachy_serial_number

import tools.network_tools as network_tools
import tools.service_app_tools as service_app_tools
import tools.dashboard_tools as dashboard_tools
import tools.common_tools as common_tools

reachy_generation = get_reachy_generation()

if reachy_generation == 2021:
    import tools.debug_tools_2021 as debug_tools
elif reachy_generation == 2023:
    import tools.debug_tools_2023 as debug_tools
else:
    print("Could not get Reachy's generation in configuration file.")
    exit()

app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(24)

import logging

logging.basicConfig(level=logging.INFO)
reachy_dashboard = dashboard_tools.ReachyDashboard()


# Render templates
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/wifi")
def wifi():
    global wifi_list
    if not net_tools.get_connection_status()["mode"] == "Hotspot":
        wifi_list = net_tools.get_available_wifis()
    return render_template(
        "wifi.html",
        wifi_list=wifi_list,
    )


@app.route("/service")
def service():
    return render_template("service.html")


@app.route("/app")
def reachy_app():
    return render_template("app.html")


@app.route("/dashboard")
def dashboard():
    global reachy_dashboard
    if not reachy_dashboard.connection_succeed:
        logging.info("Could not connect to Reachy")
    else:
        logging.info("Connected to Reachy.")
    return render_template("dashboard.html")


# Wifi API
@app.route("/update-wifi", methods=["POST"])
def update_wifi():
    if net_tools.get_connection_status()["mode"] == "Hotspot":
        net_tools.set_hotspot_state("off")

    net_tools.setup_new_wifi(request.form["ssid"], request.form["password"])
    return redirect(url_for("wifi"))


@app.route("/api/ip")
def update_ip():
    ip = net_tools.get_ip()
    net_tools.display_ip(ip)
    return Response(
        response=json.dumps(ip),
        mimetype="application/json",
    )


@app.route("/api/connection_status")
def update_connection_status():
    return Response(
        response=json.dumps(net_tools.get_connection_status()),
        mimetype="application/json",
    )


@app.route("/api/hotspot", methods=["POST"])
def toggle_hotspot():
    net_tools.set_hotspot_state(state=request.data.decode())
    if request.data.decode() == "off" and net_tools.get_connection_status()["mode"] == "None":
        net_tools.set_hotspot_state("on")
    return Response(status=200)


@app.route("/api/available_networks")
def update_available_networks():
    if net_tools.get_connection_status()["mode"] == "Hotspot":
        global wifi_list
        available_networks = wifi_list
    else:
        available_networks = net_tools.get_available_wifis()
    return Response(
        response=json.dumps(available_networks),
        mimetype="application/json",
    )


@app.route("/api/connection_card_info")
def update_connection_card_info():
    return Response(
        response=json.dumps(net_tools.get_connection_card_info()),
        mimetype="application/json",
    )


# Index API
@app.route("/api/missing_modules_names")
def get_missing_modules_names():
    return Response(
        response=json.dumps(debug_tools.get_missing_modules_names()),
        mimetype="application/json",
    )


@app.route("/api/missing_modules_bool")
def get_missing_modules_bool():
    return Response(
        response=json.dumps(debug_tools.are_missing_modules()),
        mimetype="application/json",
    )


# Service API
@app.route("/api/list_services")
def list_services():
    return Response(
        response=json.dumps(service_app_tools.list_services_or_apps(type="service")),
        mimetype="application/json",
    )


@app.route("/api/restart_service", methods=["POST"])
def restart_service():
    service_app_tools.restart_service_or_app(type="service", name=request.data.decode())
    return Response(status=200)


@app.route("/api/stop_service", methods=["POST"])
def stop_service():
    service_app_tools.stop_service_or_app(type="service", name=request.data.decode())
    return Response(status=200)


@app.route("/api/is_service_running", methods=["POST"])
def is_service_running():
    return Response(
        response=json.dumps(service_app_tools.is_service_or_app_running(type="service", name=request.data.decode())),
        mimetype="application/json",
    )


@app.route("/api/status_service", methods=["POST"])
def status_service():
    return service_app_tools.get_service_or_app_status(type="service", name=request.data.decode())


# App API
@app.route("/api/list_apps")
def list_apps():
    return Response(
        response=json.dumps(service_app_tools.list_services_or_apps(type="app")),
        mimetype="application/json",
    )


@app.route("/api/restart_app", methods=["POST"])
def restart_app():
    service_app_tools.restart_service_or_app(type="app", name=request.data.decode())
    return Response(status=200)


@app.route("/api/stop_app", methods=["POST"])
def stop_app():
    service_app_tools.stop_service_or_app(type="app", name=request.data.decode())
    return Response(status=200)


@app.route("/api/is_app_running", methods=["POST"])
def is_app_running():
    return Response(
        response=json.dumps(service_app_tools.is_service_or_app_running(type="app", name=request.data.decode())),
        mimetype="application/json",
    )


@app.route("/api/status_app", methods=["POST"])
def status_app():
    return service_app_tools.get_service_or_app_status(type="app", name=request.data.decode())


@app.route("/api/app_disable")
def disable_app():
    return Response(
        response=json.dumps(service_app_tools.list_app_to_disable()),
        mimetype="application/json",
    )


# Dashboard API
@app.route("/api/change-compliance", methods=["GET"])
async def change_compliance():
    part_req = request.args.get("part")

    compliance_req = request.args.get("compliance")

    if compliance_req == "smooth":
        await reachy_dashboard.turn_off_smoothly(part=part_req)
        return Response(status=200)

    if compliance_req == "false":
        compliance_req = False
    else:
        compliance_req = True

    reachy_dashboard.change_compliancy(part=part_req, compliance=compliance_req)
    return Response(status=200)


@app.route("/api/get-compliance-config")
def get_compliance_config():
    config = list(reachy_dashboard._compliance_config.keys())
    return Response(
        response=json.dumps(config),
        mimetype="application/json",
    )


@app.route("/api/get-fans-info")
def get_fans_info():
    return Response(
        response=json.dumps(reachy_dashboard.get_fans_info()),
        mimetype="application/json",
    )


@app.route("/api/set-fans-state", methods=["GET"])
def set_fans_state():
    fan_req = request.args.get("fan")
    state_req = request.args.get("state")

    reachy_dashboard.set_fan_state(fan=fan_req, state=state_req)
    return Response(status=200)


@app.route("/api/get-states")
def get_states():
    logging.info(json.dumps(reachy_dashboard.get_states()))
    return Response(
        response=json.dumps(reachy_dashboard.get_states()),
        mimetype="application/json",
    )


@app.route("/api/get-reachy-info")
def get_robot_info():
    return Response(
        response=json.dumps(
            {
                "model": get_reachy_model(),
                "serial_number": get_reachy_serial_number(),
            }
        ),
        mimetype="application/json",
    )


# Common tools API
@app.route("/api/shutdown")
def shutdown():
    common_tools.shutdown()
    return Response(status=200)


# Helper pages
@app.route("/reconnect_motor")
def reconnect_motor():
    return render_template("reconnect_motor.html")


@app.route("/reconnect_load_sensor")
def reconnect_load_sensor():
    return render_template("reconnect_load_sensor.html")


@app.route("/motor_control")
def control():
    return render_template("control.html")


# server.py


@app.route("/api/get_parts_and_joints")
def get_parts_and_joints():
    # Add min and max values for each joint
    data = {
        "r_arm": {
            "r_shoulder_pitch": {"min": -150, "max": 90},
            "r_shoulder_roll": {"min": -180, "max": 10},
            "r_arm_yaw": {"min": -90, "max": 90},
            "r_elbow_pitch": {"min": -125, "max": 0},
            "r_forearm_yaw": {"min": -100, "max": 100},
            "r_wrist_pitch": {"min": -45, "max": 45},
            "r_wrist_roll": {"min": -55, "max": 35},
            "r_gripper": {"min": -50, "max": 25},
        },
        "l_arm": {
            "l_shoulder_pitch": {"min": -150, "max": 90},
            "l_shoulder_roll": {"min": -10, "max": 180},
            "l_arm_yaw": {"min": -90, "max": 90},
            "l_elbow_pitch": {"min": -125, "max": 0},
            "l_forearm_yaw": {"min": -100, "max": 100},
            "l_wrist_pitch": {"min": -45, "max": 45},
            "l_wrist_roll": {"min": -35, "max": 55},
            "l_gripper": {"min": -25, "max": 50},
        },
    }

    return json.dumps(data)


@app.route("/api/trigger_event", methods=["POST"])
def trigger_event():
    data = request.get_json()
    part = data["part"]
    slider_values = data["sliderValues"]
    duration = data["duration"]  # Get the duration from the received data

    # Log the received data
    logging.info(f"Received data for part {part} with slider values {slider_values} and duration {duration}")
    reachy_dashboard = dashboard_tools.ReachyDashboard()
    cmd = {k: float(v) for k, v, in slider_values.items()}
    # cmd = {"r_elbow_pitch" : 45}
    logging.info(cmd)
    reachy_dashboard.set_goal_position(cmd)
    # Your code to handle the event goes here

    return Response(status=200)


@app.route("/api/record_pose", methods=["POST"])
def record_pose():
    data = request.get_json()
    part = data["part"]
    slider_values = data["sliderValues"]
    duration = data["duration"]
    pose_name = data["poseName"]

    logging.info(f"Received pose {pose_name} for part {part} with slider values {slider_values} and duration {duration}")

    # Your code to handle the event goes here

    return Response(status=200)


@app.route("/api/set_joint_value", methods=["GET"])
def set_joint_value():
    part = request.args.get("part")
    joint = request.args.get("joint")
    value = request.args.get("value")

    # This is where you call your function
    # Assuming that your function expects the value to be a float in the range [0, 1]
    value = float(value) / 100.0
    goto_dict = {joint: value}
    goto(goto_dict, duration=0.1)

    return Response(status=200)


if __name__ == "__main__":
    # time.sleep(10.0)

    print("Starting Reachy dashboard...")

    net_tools = network_tools.NetworkTools()

    connection_status = net_tools.get_connection_status()["mode"]

    if not (connection_status == "Wifi" or connection_status == "Ethernet"):
        net_tools.set_hotspot_state("off")
        wifi_list = net_tools.get_available_wifis()
        net_tools.set_hotspot_state("on")

    else:
        wifi_list = net_tools.get_available_wifis()

    net_tools.display_ip(net_tools.get_ip())
    app.run(host="0.0.0.0", port=3972, debug=True)
