import usb.core
import usb.util
import sys

dev = usb.core.find(idVendor=0x0fe6, idProduct=0x811e)
# dev = usb.core.find(idVendor=0x3f4, idProduct=0x2009, find_all=True)

for printer in usb.core.find(find_all=True, bDeviceClass=7):
    print(printer)

# cfg = dev.get_active_configuration()
# intf = cfg[(0, 0)]
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
# )
#
# print(ep)
# dev.reset()
