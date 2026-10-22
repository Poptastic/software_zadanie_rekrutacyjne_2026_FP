from nicegui import ui
import sys
import subprocess

sim_process = None

def apk_set_up():
    ui.label('TEST')
    ui.run(reload=False)
    proxy_process = subprocess.Popen([sys.executable, "tcp_proxy.py"])
    ui.button('stop sim', on_click=lambda: sim_start_stop_handler(0))
    ui.button('start sim', on_click=lambda: sim_start_stop_handler(1))

def sim_start_stop_handler(state: int):
    global sim_process
    if state == 1 and sim_process == None:
        sim_process = subprocess.Popen([sys.executable, "tcp_simulator.py"])
    if state == 0:
        if sim_process == None:
            return
        sim_process.terminate()
        sim_process = None


def stop_sim(process):
    #global sim_process
    if process == None:
        return
    process.terminate()

apk_set_up()