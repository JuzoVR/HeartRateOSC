import asyncio
from logging import shutdown
import math
import os
import signal
import sys
import time

from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc import dispatcher

from bleak import BleakScanner, BleakClient
from bleak.uuids import uuid16_dict


## CHANGE THIS TO YOUR MAC ADDRESS. Should be like **:**:**:**:**:**
ADDRESS = "CHANGE THIS TO YOUR MAC ADDRESS FOR YOUR DEVICE"

uuid16_dict = {v: k for k, v in uuid16_dict.items()}

## UUID for model number ##
MODEL_NBR_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Model Number String")
)


## UUID for manufacturer name ##
MANUFACTURER_NAME_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Manufacturer Name String")
)

## UUID for battery level ##
BATTERY_LEVEL_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Battery Level")
)

## UUID for connection establsihment with device ##
PMD_SERVICE = "FB005C80-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Request of stream settings ##
PMD_CONTROL = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Request of start stream ##
PMD_DATA = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Heart rate 

HR_UUID = "0000{0:x}-0000-1000-8000-00805F9B34FB".format(
    uuid16_dict.get("Heart Rate Measurement")
)

## UUID for Request of ECG Stream ##
ECG_WRITE = bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0E, 0x00])

## For Plolar H10  sampling frequency ##
ECG_SAMPLING_FREQ = 130

SHUTDOWN = False

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

def stop(signum, frame):
    global SHUTDOWN
    print('STOP', signum)
    SHUTDOWN = True
    print('STOP2')

signal.signal(signal.SIGTERM, stop)


async def data_callback(sender, data):
    
    hr = abs(int.from_bytes(
        bytearray(data[1:2]), byteorder="little", signed=True,
    ))
    # HR = absolute value of the heart rate bpm from the monitor. 
    upper_bound = 180
    heart_rate_normalized = min([float(hr/upper_bound),1])
    # Normalized the heart rate for animations. (0-1 with a max of 180 bpm))
    
    
    # Change this parameter to whatever your avatar uses
    parameter = "/avatar/parameters/OSCBlink"
    
    osc_client.send_message(parameter,heart_rate_normalized)
    
    # print("current hr and speed", hr, heart_rate_normalized)

async def main(address):
    ## Writing chracterstic description to control point for request of UUID (defined above) ##
    async with BleakClient(address) as client:
        await client.is_connected()
        print("---------Device connected--------------Juzo")

        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

        manufacturer_name = await client.read_gatt_char(MANUFACTURER_NAME_UUID)
        print("Manufacturer Name: {0}".format("".join(map(chr, manufacturer_name))))

        battery_level = await client.read_gatt_char(BATTERY_LEVEL_UUID)
        print("Battery Level: {0}%".format(int(battery_level[0])))

        att_read = await client.read_gatt_char(PMD_CONTROL)

        await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)

        ## ECG stream started
        await client.start_notify(HR_UUID, data_callback)
        n = 0
        while not SHUTDOWN:
            await asyncio.sleep(1)
            n += 1
            if n % 60 == 0:
                minutes = n/60
                print("App has been running for ", minutes, " minutes")
            
        sys.exit(0)



async def init_main():
    await main(ADDRESS)  # Enter main loop of program

asyncio.run(init_main())