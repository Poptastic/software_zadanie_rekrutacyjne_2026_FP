from nicegui import ui
import sys
import json
import os
import subprocess
from pathlib import Path

#sys.path.append(str(Path(__file__).resolve().parent.parent))


sim_process = None
rocket_status_file = "rocket_status.json"
error_messages = "error_messages.json"

def apk_set_up():
    ui.label('TEST')

    sim_info()
    error_info()

    ui.button(
        'stop sim', on_click=lambda: sim_start_stop_handler(0)
        )
    
    ui.button(
        'start sim', on_click=lambda: sim_start_stop_handler(1)
        )
    
    ui.timer(0.001, sim_info.refresh)
    ui.timer(0.001, error_info.refresh)

    ui.run()
    proxy_process = subprocess.Popen([sys.executable, "./tcp_proxy.py"])

def sim_start_stop_handler(state: int):
    global sim_process
    global rocket_status_file
    if state == 1 and sim_process == None:
        sim_process = subprocess.Popen([sys.executable, "./tcp_simulator.py"])
    if state == 0:
        if sim_process == None:
            return
        sim_process.terminate()
        sim_process = None
        os.remove("rocket_status.json")
        os.remove("error_messages.json")

@ui.refreshable
def sim_info():
    try:
        with open(rocket_status_file, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ui.label('Awaiting data...')
        return

    ui.label(f"Rocket state: {status['state']}")

    ui.label("Sensors:")
    ui.label(f"-Fuel level: {status['sensors']['fuel_level']:.1f}%")
    ui.label(f"-Oxidizer level: {status['sensors']['oxidizer_level']:.1f}%")
    ui.label(f"-Oxidizer pressure: {status['sensors']['oxidizer_pressure']:.1f} bar")
    ui.label(f"-Altitude: {status['sensors']['altitude']:.1f} m")
    ui.label(f"-Angle: {status['sensors']['angle']:.1f}°")

@ui.refreshable
def error_info():
    try:
        with open(error_messages, 'r') as f:
            messages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    ui.label('errors:')
    if len(messages) == 0:
        ui.label('NO ERRORS')
    else:
        ui.label(messages[0])


apk_set_up()