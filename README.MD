# Heart rate monitor to OSC VRChat

This is for use with Polar H10

### Initial Steps

- `pip install -r requirements.txt`
- `python ./getDevice.py`
    - Take note of the MAC ADDRESS of your heart rate monitor.
- Open `heart.py` 
    1. Replace line 18 `ADDRESS` with the mac address from `getDevice.py`
    2. In `data_callback` you can replace the `parameter` with however your avi is using parameters. Usually it will be `/avatar/parameter/{field}`. 
    3. Choose your `upper_bound`. I chose 180 bpm as my upper bound. Its divisible by 60 which works better for unity. You need to have floats that are less than 1 but greater than 0 to pass over to OSC. 
    4. To debug and make sure its running uncomment `line 88.` 
    5. To Exit spam `ctrl + c`. I don't know how to do a graceful exit and my shutdown method does not work.
    6. Use `python ./heart.py` to run the OSC. To start you may have to run it a few times. Make sure you have your hr monitor on. If you don't see it in `getDevices` then something is wrong with your bluetooth or the monitor. 
    7. Start VRChat, be opted into the OSC beta (if during the open beta) and turn on OSC in the quick menu.

This SHOULD work.
