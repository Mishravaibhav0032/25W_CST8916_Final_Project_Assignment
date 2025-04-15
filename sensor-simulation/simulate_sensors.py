import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

devices = {
    "Dow's Lake": "HostName=Rideau-IOT-Hub.azure-devices.net;DeviceId=DowsLakeSensor;SharedAccessKey=sgNW9YYrtxDF9DSUe74Z89DnXCnQvTx/+R2cFsXIiUk=",
    "Fifth Avenue": "HostName=Rideau-IOT-Hub.azure-devices.net;DeviceId=FifthaveSensor;SharedAccessKey=fyN1u0aGXVvjUWV2cQwCNzdTQ0OTgRmfb6d8jCvPEvc=",
    "NAC": "HostName=Rideau-IOT-Hub.azure-devices.net;DeviceId=NACSensor;SharedAccessKey=FZAmPZqMW9hjAnqYp/gXK0We8zMVKPwPVmx/jwvMhoI="
}

def generate_payload(location):
    payload = {
        "location": location,
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": random.randint(-10, 2),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": random.randint(-15, 5),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return payload

def send_data():
    while True:
        for location, conn_str in devices.items():
            client = IoTHubDeviceClient.create_from_connection_string(conn_str)
            payload = generate_payload(location)
            msg = Message(str(payload))
            print(f"Sending from {location}: {msg}")
            client.send_message(msg)
            client.disconnect()
        time.sleep(10)

if __name__ == "__main__":
    send_data()

