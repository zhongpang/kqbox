# -*- coding:utf-8 -*-
##
 #  @filename   :   main.cpp
 #  @brief      :   2.13inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy

import epd2in13b
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#import imagedata

COLORED = 1
UNCOLORED = 0

def main():
    epd = epd2in13b.EPD()
    epd.init()
    # clear the frame buffer
    frame_black = [0xFF] * (epd.width * epd.height / 8)
    frame_red = [0xFF] * (epd.width * epd.height / 8)
    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in13b.EPD_WIDTH, epd2in13b.EPD_HEIGHT), 255)  # 255: clear the frame
    #image = image.rotate(90)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
    draw.rectangle((0, 10, 128, 30), fill = 0)
    draw.text((20, 14), 'Hello world!', font = font, fill = 255)
    draw.text((20, 36), 'e-Paper Demo', font = font, fill = 0)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wyq/wqy-microhei.ttc', 18)
    draw.text((10, 56), u'你好，树莓派', font = font, fill = 0)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wyq/wqy-zenhei.ttc', 24)
    draw.text((20, 80), u'微雪电子', font = font, fill = 0)
    print "你好"
	
    #epd.clear_frame_memory(0xFF)
    #epd.set_frame_memory(image , 0, 0)
    epd.display_frame(frame_black, frame_red)

    epd.delay_ms(2000)

if __name__ == '__main__':
    main()
