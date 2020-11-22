#!/usr/bin/env python

'''
 THIS IS SCRIPT IS USING A UDEV RULES WHICH MOUNTS USB AUTOMATICALLY AND THEN WE ARE POLLING LIST
 OF DEVICES FROM UDEV RULES THIS IS HOW IT WORKS
'''
import pyudev, psutil, time
from os import walk
context = pyudev.Context()
def poll_devices():
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    for device in removable:
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        print("All removable partitions: {}".format(", ".join(partitions)))
        print("Mounted removable partitions:")
        for p in psutil.disk_partitions():
            if p.device in partitions:
                print("  {}: {}".format(p.device, p.mountpoint))
                f = []
                for (dirpath, dirnames, filenames) in walk(p.mountpoint):
                    f.extend(filenames)
                    break
                print (f)

while 1:
    poll_devices()
    time.sleep(1)