import usb.core
import time
import os
import subprocess
import pygame
from pygame.locals import *
import os.path
import signal
import logging

# Skip these to workaround https://github.com/pygame/pygame/issues/342
def handler(signum, frame):
  """Why is systemd sending sighups? I DON'T KNOW."""
  logging.warning("Got a {} signal. Doing nothing".format(signum))

signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGCONT, handler)

WHITE = (255,255,255)
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
font_big = pygame.font.Font(None, 50)
message = ''
old_message = None

def redraw():
    global message, old_message
    if message == old_message:
        return
    print("redraw '%s'" % message)
    lcd.fill((0,0,0))
    text_surface = font_big.render(message, True, WHITE)
    rect = text_surface.get_rect(center=(160,120))
    lcd.blit(text_surface, rect)
    pygame.display.update()
    old_message = message

first_run = True
process = None

while True:
    redraw()
    dev = usb.core.find(idVendor=0x04c5, idProduct=0x128d)

    if process != None:
        print(process.pid)
        if process.poll() != None:
            process = None
            message = "No scanner"

    if dev is None:
        message = ""
        if process != None:
            first_run = False
            process.terminate()
        time.sleep(2)
        continue
    
    if process == None:
        message = "Scanner on"
        process = subprocess.Popen(["/usr/sbin/scanbd", "-f", "-d3"], env={"SCANBD_DEVICE": "epjitsu:libusb:%03d:%03d" % (dev.bus, dev.address)})
    else:
        scan_status_file = "/tmp/scan-status"
        if os.path.exists(scan_status_file):
            message = open(scan_status_file).read().strip()
        elif first_run:
            message = "Scanner on"
        else:
            message = "Scan ended"
        time.sleep(2)
