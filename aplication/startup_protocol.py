import sys
from pathlib import Path
import asyncio

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

    relay_open_frame = Frame(ids.BoardID.ROCKET, 
                            ids.PriorityID.LOW, 
                            ids.ActionID.SERVICE, 
                            ids.BoardID.SOFTWARE, 
                            ids.DeviceID.RELAY, 
                            0, # oxidizer heater
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.RELAY.value.OPEN,
                            ()
                            )
    cm.push(relay_open_frame) # We need to push the frame onto the send queue

    servo_open_frame = relay_open_frame = Frame(ids.BoardID.ROCKET, 
                               ids.PriorityID.LOW, 
                               ids.ActionID.SERVICE, 
                               ids.BoardID.SOFTWARE, 
                               ids.DeviceID.SERVO, 
                               1, # oxidizer intake 
                               ids.DataTypeID.INT16,
                               ids.OperationID.SERVO.value.POSITION,
                               (0,) # 0 is for open position, 100 is for closed
                               )
    cm.push(servo_open_frame)

def frame_handler():
    try:
        frame = cm.receive()
    except TransportTimeoutError:
        pass
    except UnregisteredCallbackError as e:
        print(f"unregistered frame received: {e.frame}")
    cm.send()

async def instructions_executer():
    global cm
    await asyncio.sleep(2.0)
    frame_handler()
    await asyncio.sleep(2.0)
    frame_handler()
    #CM WORKING AS LIFO

asyncio.run(instructions_executer())

