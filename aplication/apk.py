from nicegui import ui, Client, app
import sys
import json
import os
import subprocess
import atexit


ui.label('TEST')

awaiting_sim_label = ui.label('Waiting for sim to start...')

sim_process = None
proxy_process = None
rocket_status_file = "./rocket_status.json"
error_messages = "./error_messages.json"

def apk_set_up():
    global proxy_process
    global labels_container

    sim_info()

    with ui.column().classes('items-center'):
        labels_container = ui.column().classes('items-left')

    with ui.row().classes('h-96'):
        ui.button(
            'stop sim', on_click=lambda: sim_start_stop_handler(0)
            )
    
        ui.button(
            'start sim', on_click=lambda: sim_start_stop_handler(1)
            )
    
    ui.timer(0.1, sim_info.refresh)
    ui.timer(0.1, error_info.refresh)

    proxy_process = subprocess.Popen([sys.executable, "./tcp_proxy.py"])

def sim_start_stop_handler(state: int):
    global rocket_status_file
    global sim_process
    global rocket_state
    global fuel_level
    global oxidizer_level
    global oxidizer_pressure
    global altitude
    global angle
    global fuel_intake
    global oxidizer_intake
    global fuel_main
    global oxidizer_main
    global oxidizer_heater
    global igniter
    global parachute
    global velocity

    if state == 1 and sim_process == None:

        labels_container.clear()
        
        awaiting_sim_label.set_text('')

        sim_process = subprocess.Popen([sys.executable, "./tcp_simulator.py"])

        with labels_container:
            with ui.row().classes('items-center'):
                ui.label(f"Rocket state: ")
                rocket_state = ui.label('')
            ui.label("Sensors:")
            with ui.row().classes('items-center'):
                ui.label(f"     -Fuel level: ")
                fuel_level = ui.label('')
                ui.label("%")
            with ui.row().classes('items-center'):
                ui.label(f"     -Oxidizer level: ")
                oxidizer_level = ui.label('')
                ui.label("%")
            with ui.row().classes('items-center'):
                ui.label("      -Oxidizer pressure: ")
                oxidizer_pressure = ui.label('')
                ui.label(' bar')
            with ui.row().classes('items-center'):
                ui.label(f"     -Altitude: ")
                altitude = ui.label('')
                ui.label(" m")
            with ui.row().classes('items-center'):
                ui.label(f"     -Angle: ")
                angle = ui.label('')
                ui.label("°")
            ui.label('Servos:')
            with ui.row().classes('items-center'):
                ui.label("      -Fuel intake: ")
                fuel_intake = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("      -Oxidizer intake: ")
                oxidizer_intake = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("      -Fuel main: ")
                fuel_main = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("      -Oxidizer main: ")
                oxidizer_main = ui.label('')
            ui.label('Relays:')
            with ui.row().classes('items-center'):
                ui.label("      -Oxidizer heater: ")
                oxidizer_heater = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("      -Igniter: ")
                igniter = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("      -Parachute: ")
                parachute = ui.label('')
            with ui.row().classes('items-center'):
                ui.label("Velocity: ")
                velocity = ui.label('')
                ui.label("m/s")
            ui.label('Errors:')
            error_info()
    
    if state == 0:
        if sim_process == None:
            return
        labels_container.clear()
        awaiting_sim_label.set_text('Waiting for sim to start...')
        sim_process.terminate()
        sim_process = None
        os.remove("rocket_status.json")
        os.remove("error_messages.json")

@ui.refreshable
def sim_info():
    global rocket_status_file
    #global rocket_state
    #global fuel_level
    #global oxidizer_level
    #global oxidizer_pressure
    #global altitude
    #global angle

    try:
        with open(rocket_status_file, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    rocket_state.set_text(f"{status['state']}")
    fuel_level.set_text(f"{status['sensors']['fuel_level']:.1f}")
    oxidizer_level.set_text(f"{status['sensors']['oxidizer_level']:.1f}")
    oxidizer_pressure.set_text(f"{status['sensors']['oxidizer_pressure']:.1f}")
    altitude.set_text(f"{status['sensors']['altitude']:.1f}")
    angle.set_text(f"{status['sensors']['angle']:.1f}")
    fuel_intake.set_text(f"{status['servos']['fuel_intake']}")
    oxidizer_intake.set_text(f"{status['servos']['oxidizer_intake']}")
    fuel_main.set_text(f"{status['servos']['fuel_main']}")
    oxidizer_main.set_text(f"{status['servos']['oxidizer_main']}")
    oxidizer_heater.set_text(f"{'OPEN' if status['relays']['oxidizer_heater'] else 'CLOSED'}")
    igniter.set_text(f"{'OPEN' if status['relays']['igniter'] else 'CLOSED'}")
    parachute.set_text(f"{'OPEN' if status['relays']['parachute'] else 'CLOSED'}")
    velocity.set_text(f"{status['velocity']:.2f}")


@ui.refreshable
def error_info():
    try:
        with open(error_messages, 'r') as f:
            messages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    if len(messages) == 0:
        ui.label('NO ERRORS')
    else:
        for i in messages:
            ui.label(i)

def clean_up():
    proxy_process.terminate()
    if sim_process != None:
        sim_process.terminate()
        os.remove("rocket_status.json")
        os.remove("error_messages.json")

apk_set_up()

atexit.register(clean_up)

ui.run()