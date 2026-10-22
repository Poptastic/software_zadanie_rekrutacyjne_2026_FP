from nicegui import ui
import sys
import json
import os
import subprocess

sim_process = None
rocket_status_file = "rocket_status.json"

def apk_set_up():
    ui.label('TEST')

    sim_info()

    ui.button(
        'stop sim', on_click=lambda: sim_start_stop_handler(0)
        )
    
    ui.button(
        'start sim', on_click=lambda: sim_start_stop_handler(1)
        )
    
    ui.timer(0.5, sim_info.refresh)
    
    ui.run(reload=False)
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

@ui.refreshable
def sim_info():
    try:
        with open(rocket_status_file, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ui.label('awaiting data...')
        return

    ui.label(f"Rocket state: {status['state']}")

apk_set_up()