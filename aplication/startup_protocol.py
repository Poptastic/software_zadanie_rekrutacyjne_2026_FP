import sys
from pathlib import Path
import asyncio
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError

cm = CommunicationManager()
cm.change_transport_type(TransportType.TCP)


def on_altitude(frame: Frame):
    print(f"Registered frame received: {frame}")

if __name__ == "__main__":

    status = None

    try:
        with open("./rocket_status.json", 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    cm = CommunicationManager()
    cm.change_transport_type(TransportType.TCP)

    altitude_frame = Frame(ids.BoardID.SOFTWARE, 
                            ids.PriorityID.LOW, 
                            ids.ActionID.FEED, 
                            ids.BoardID.ROCKET, 
                            ids.DeviceID.SENSOR, 
                            2, # altitude sensor
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.SENSOR.value.READ)
    cm.register_callback(on_altitude, altitude_frame)
    cm.connect(TcpSettings("127.0.0.1", 3000))

    oxidizer_intake_open_frame = Frame(ids.BoardID.ROCKET, 
                               ids.PriorityID.LOW, 
                               ids.ActionID.SERVICE, 
                               ids.BoardID.SOFTWARE, 
                               ids.DeviceID.SERVO, 
                               1, # oxidizer intake 
                               ids.DataTypeID.INT16,
                               ids.OperationID.SERVO.value.POSITION,
                               (0,) # 0 is for open position, 100 is for closed
                               )
    cm.push(oxidizer_intake_open_frame)

    oxidizer_intake_close_frame = Frame(ids.BoardID.ROCKET, 
                                   ids.PriorityID.LOW, 
                                   ids.ActionID.SERVICE, 
                                   ids.BoardID.SOFTWARE, 
                                   ids.DeviceID.SERVO, 
                                   1, # oxidizer intake 
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (100,) # 0 is for open position, 100 is for closed
                                   )

    cm.push(oxidizer_intake_close_frame)

    fuel_intake_open_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (0,))

    cm.push(fuel_intake_open_frame)

    fuel_intake_close_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (100,))

    cm.push(fuel_intake_close_frame)

    oxidizer_heater_open_frame = Frame(ids.BoardID.ROCKET, 
                                ids.PriorityID.LOW, 
                                ids.ActionID.SERVICE, 
                                ids.BoardID.SOFTWARE, 
                                ids.DeviceID.RELAY, 
                                0, # oxidizer heater
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.RELAY.value.OPEN,
                                ()
                                )
    
    cm.push(oxidizer_heater_open_frame)

    oxidizer_heater_close_frame = Frame(ids.BoardID.ROCKET, 
                                    ids.PriorityID.LOW, 
                                    ids.ActionID.SERVICE, 
                                    ids.BoardID.SOFTWARE, 
                                    ids.DeviceID.RELAY, 
                                    0, # oxidizer heater
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.RELAY.value.CLOSE,
                                    ()
                                    )
        
    cm.push(oxidizer_heater_close_frame)

    fuel_main_open_frame = Frame(ids.BoardID.ROCKET,
                           ids.PriorityID.LOW,
                           ids.ActionID.SERVICE,
                           ids.BoardID.SOFTWARE,
                           ids.DeviceID.SERVO,
                           2,
                           ids.DataTypeID.INT16,
                           ids.OperationID.SERVO.value.POSITION,
                           (0,))
    
    cm.push(fuel_main_open_frame)

    oxidizer_main_open_frame = Frame(ids.BoardID.ROCKET,
                               ids.PriorityID.LOW,
                               ids.ActionID.SERVICE,
                               ids.BoardID.SOFTWARE,
                               ids.DeviceID.SERVO,
                               3,
                               ids.DataTypeID.INT16,
                               ids.OperationID.SERVO.value.POSITION,
                               (0,))
    
    cm.push(oxidizer_main_open_frame)

    igniter_open_frame = Frame(ids.BoardID.ROCKET,
                               ids.PriorityID.LOW,
                               ids.ActionID.SERVICE,
                               ids.BoardID.SOFTWARE,
                               ids.DeviceID.RELAY,
                               1,
                               ids.DataTypeID.FLOAT,
                               ids.OperationID.RELAY.value.OPEN,
                               ())

    cm.push(igniter_open_frame)

    fuel_main_close_frame = Frame(ids.BoardID.ROCKET,
                               ids.PriorityID.LOW,
                               ids.ActionID.SERVICE,
                               ids.BoardID.SOFTWARE,
                               ids.DeviceID.SERVO,
                               2,
                               ids.DataTypeID.INT16,
                               ids.OperationID.SERVO.value.POSITION,
                               (100,))
        
    cm.push(fuel_main_close_frame)

    oxidizer_main_close_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   3,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (100,))
        
    cm.push(oxidizer_main_close_frame)

    igniter_close_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.RELAY,
                                   1,
                                   ids.DataTypeID.FLOAT,
                                   ids.OperationID.RELAY.value.CLOSE,
                                   ())
    
    cm.push(igniter_close_frame)

    parachute_open_frame = Frame(ids.BoardID.ROCKET,
                                 ids.PriorityID.LOW,
                                 ids.ActionID.SERVICE,
                                 ids.BoardID.SOFTWARE,
                                 ids.DeviceID.RELAY,
                                 2,
                                 ids.DataTypeID.FLOAT,
                                 ids.OperationID.RELAY.value.OPEN,
                                 ())

    cm.push(parachute_open_frame)

    
def frame_handler():
    try:
        frame = cm.receive()
    except TransportTimeoutError:
        pass
    except UnregisteredCallbackError as e:
        print(f"unregistered frame received: {e.frame}")
    cm.send()

async def conditioner(statement):
    global status
    while True:
        await asyncio.sleep(0.1)
        try:
            with open("./rocket_status.json", 'r') as f:
                status = json.loads(f.readline())
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        if statement(status):
            break
    return

async def instructions_executer():
    global cm
    await asyncio.sleep(2.0)
    #oxidizer intake open
    frame_handler()
    #wait for it to fill
    await conditioner(lambda status: status['sensors']['oxidizer_level'] == 100.0)
    #oxidizer intake close
    frame_handler()
    #fuel intake open
    frame_handler()
    #wait for fuel to fill
    await conditioner(lambda status: status['sensors']['fuel_level'] == 100.0)
    #fuel intake close
    frame_handler()
    #oxidizer heater open
    frame_handler()
    #wait for it to heat up
    await conditioner(lambda status: status['sensors']['oxidizer_pressure'] >= 65.0)
    #oxidizer heater close
    frame_handler()
    await asyncio.sleep(0.1)
    #fuel main open
    frame_handler()
    #oxidizer main open
    await asyncio.sleep(0.1)
    frame_handler()
    #igniter open
    await asyncio.sleep(0.1)
    frame_handler()
    #wait for apogee
    await conditioner(lambda status: status['state'] == 'APOGEE')
    #close all
    frame_handler()
    await asyncio.sleep(0.1)
    frame_handler()
    await asyncio.sleep(0.1)
    frame_handler()
    #wait for correct speed
    await conditioner(lambda status: status['velocity'] <= 30.0)
    #open parachute
    frame_handler()



        

asyncio.run(instructions_executer())

