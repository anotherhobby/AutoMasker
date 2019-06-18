from m5stack import *
from m5ui import *
from uiflow import *
import unit
import math
import time

# set screen size and a startup mask of "open"
screenh_in = 55
screenw_in = 132
current = "open"

# screen aspect ratios
aspect_ratios = {
    "open": {"name": "Open Screen", "ratio": 2.43},
    "anamorph24": {"name": "Anamorphic 2.4:1", "ratio": 2.4},
    "anamorph239": {"name": "Anamorphic 2.39:1", "ratio": 2.39},
    "anamorph235": {"name": "Anamorphic 2.35:1", "ratio": 2.35},
    "widescreen": {"name": "Widescreen 1.85:1", "ratio": 1.85},
    "hdtv": {"name": "HDTV 16:9", "ratio": 1.77},
    "computer": {"name": "Computer 16:10", "ratio": 1.6},
    "sdtv": {"name": "SDTV 4:3", "ratio": 1.33}
    }

# make an ordered list of aspect_ratios sorted by ratio
aspects = sorted(aspect_ratios, key=lambda x: (aspect_ratios[x]['ratio']), reverse=True)

# setup display
setScreenColor(0x000000)
title1 = M5Title(title="AutoMasker Screen Controller", x=4 , fgcolor=0xffffff, bgcolor=0x4343eb)
label1 = M5TextBox(10, 30, "Aspect:", lcd.FONT_DejaVu18,0xFFFFFF, rotate=0)
label2 = M5TextBox(10, 50, "Size:", lcd.FONT_Ubuntu,0xFFFFFF, rotate=0)
label3 = M5TextBox(10, 70, "Last:", lcd.FONT_Ubuntu,0xFFFFFF, rotate=0)
label4 = M5TextBox(10, 100, 'Masking {}"x{}" Screen'.format(screenw_in, screenh_in), lcd.FONT_DejaVu18,0xFFFFFF, rotate=0)
label5 = M5TextBox(10, 120, "Mask Width:", lcd.FONT_Ubuntu,0xFFFFFF, rotate=0)
label6 = M5TextBox(10, 140, "From Last:", lcd.FONT_Ubuntu,0xFFFFFF, rotate=0)
label7 = M5TextBox(10, 160, "Moved:", lcd.FONT_Ubuntu,0xFFFFFF, rotate=0)
menuMinus = M5TextBox(51, 212, "Prev", lcd.FONT_Default,0x00ff3b, rotate=0)
# menuMode = M5TextBox(134, 212, "----", lcd.FONT_Default,0xfffc00, rotate=0)
menuPlus = M5TextBox(236, 212, "Next", lcd.FONT_Default,0x00ff3b, rotate=0)

# function for call back when button A is pressed
def buttonA_wasPressed():
    move_mask(prev_item(aspects, current))
# create call back for above function when button is actually pressed
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
    pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
    move_mask(next_item(aspects, current))
btnC.wasPressed(buttonC_wasPressed)

# def inchs_to_mm(inches):
#     mm = round(inches * 25.4)
#     return mm

# calculate width of mask for a given screen width
def mask_width(target_w):
    return round((screenw_in - target_w)/2, 2)

# calculate the width of the screen for a given ratio
def ratio_width(ratio):
    return round((screenh_in * ratio), 2)

# calculate diagonal distance of a given screen size
def diagonal(w, h):
    return round(math.sqrt((w **2)+(h **2)))

# iterate forward through the organized list of screen ratios
def next_item(itemlist, item):
    found = False
    for l in itemlist:
        if found:
            return l
        elif l is item:
            found = True
    return itemlist[0]

# iterate backward through the organized list of screen ratios
def prev_item(itemlist, item):
    revlist = itemlist.copy()
    revlist.reverse()
    found = False
    for l in revlist:
        if found:
            return l
        elif l is item:
            found = True
    return revlist[0]

# function to determine how to move from one mask to another
def move_mask(aspect_ratio="anamorph24"):
    global current
    current_mask = mask_width(ratio_width(aspect_ratios[current]['ratio']))
    target_mask = mask_width(ratio_width(aspect_ratios[aspect_ratio]['ratio']))
    new_screenw_in = ratio_width(aspect_ratios[current]['ratio'])
    target_name = aspect_ratios[aspect_ratio]['name']
    if current_mask > target_mask:
        difference = current_mask - target_mask
        direction = 'OUT'
    else:
        difference = target_mask - current_mask
        direction = 'IN'
    label1.setText("Aspect: {}".format(target_name))
    label2.setText('Size: {}"x{}" @ {}" diagonal'.format(new_screenw_in, screenh_in, diagonal(new_screenw_in, screenh_in)))
    label3.setText("Last: {}".format(aspect_ratios[current]['name']))
    label5.setText('Mask Width: {}"'.format(target_mask))
    label6.setText('From Last: {}"'.format(difference))
    label7.setText('Moved: {}'.format(direction))
    current = aspect_ratio
