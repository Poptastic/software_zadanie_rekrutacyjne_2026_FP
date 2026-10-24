import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError



def on_altitude(frame: Frame):
    print(f"Registered frame received: {frame}")

if __name__ == "__main__":
    cm = CommunicationManager()
    cm.change_transport_type(TransportType.TCP)