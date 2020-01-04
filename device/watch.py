import usb.core
import time
import os
import subprocess

process = None

while True:
    dev = usb.core.find(idVendor=0x04c5, idProduct=0x128d)

    if process != None:
        print(process.pid)
        if process.poll() != None:
            process = None

    if dev is None:
        print("No scanner")
        if process != None:
            process.terminate()
        time.sleep(2)
        continue
    
    if process == None:
        process = subprocess.Popen(["/usr/sbin/scanbd", "-f", "-d3"], env={"SCANBD_DEVICE": "epjitsu:libusb:%03d:%03d" % (dev.bus, dev.address)})
    else:
        time.sleep(2)
