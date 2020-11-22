import glib
import psutil
import time
from pyudev import Context, Monitor
context = Context()
try:
    from pyudev.glib import MonitorObserver
    
    def device_event(observer, device):
        print ('\n\nevent {0} on device {1}'.format(device.action, device))
        time.sleep(3)
        print("device details",device.device_node)
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        print("All removable partitions: {}".format(", ".join(partitions)))
        print("Mounted removable partitions:")
        for p in psutil.disk_partitions():
            if p.device in partitions:
                print("  {}: {}".format(p.device, p.mountpoint))
except Exception as e:
    print ("error :",e)
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        print ('event {0} on device {1}'.format(action, device))


monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

glib.MainLoop().run()
