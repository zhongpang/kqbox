# -*- coding:utf-8 -*-
##
 #  @filename   :   main.cpp
 #  @brief      :   2.13inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
import time
import decimal 
from decimal import Decimal 
import serial
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import epd2in13b
#import imagedata

COLORED = 1
UNCOLORED = 0

def main():

    epd = epd2in13b.EPD()
    epd.init()

    # clear the frame buffer
    frame_black = [0xFF] * int(epd.width * epd.height / 8)
    frame_red = [0xFF] * int(epd.width * epd.height / 8)


    # display images
    #frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
    frame_red = epd.get_frame_buffer(Image.open('black.bmp'))
    epd.display_frame(frame_black, frame_red)

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)
    # clear the frame buffer
    #frame_black = [0xFF] * int(epd.width * epd.height / 8)
    #frame_red = [0xFF] * int(epd.width * epd.height / 8)
    epd.set_rotate(1)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wyq/wqy-microhei.ttc', 16)

    #start to get air data
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    print(ser.port)
    print(ser.baudrate)
    refreshlcd = 0
    data = []
    try:
        while True:
            print ("----------------------------------------------")
            datalen = ser.inWaiting()
            #print ("datalen:", datalen)
            if datalen !=0:
                #Read
                data = ser.read(datalen)
                ser.flushInput()
                #print 'received:', data
                bit_head = data[0]
                bit_funcd= data[1]
                bit_len  = data[2]
                int_CO2_H = int.from_bytes(data[3:4], byteorder='big')
                int_CO2_L = int.from_bytes(data[4:5], byteorder='big')
                co2 = int_CO2_H * 256 + int_CO2_L
                int_TVOC_H = int.from_bytes(data[5:6], byteorder='big')
                int_TVOC_L = int.from_bytes(data[6:7], byteorder='big')
                tvoc = (int_TVOC_H * 256 + int_TVOC_L)/10.0
                int_CH2O_H = int.from_bytes(data[7:8], byteorder='big')
                int_CH2O_L = int.from_bytes(data[8:9], byteorder='big')
                ch2o = (int_CH2O_H * 256 + int_CH2O_L)/10.0
                int_PM25_H = int.from_bytes(data[9:10], byteorder='big')
                int_PM25_L = int.from_bytes(data[10:11], byteorder='big')
                pm25 = int_PM25_H * 256 + int_PM25_L
                int_humidity_H = int.from_bytes(data[11:12], byteorder='big')
                int_humidity_L = int.from_bytes(data[12:13], byteorder='big')
                humidity = Decimal(-6 + 125 * (int_humidity_H*256+int_humidity_L)/(2**16)).quantize(Decimal('0.0'))
                int_temp_H = int.from_bytes(data[13:14], byteorder='big')
                int_temp_L = int.from_bytes(data[14:15], byteorder='big')
                temperature =Decimal(-46.84 + 175.72 * (int_temp_H*256+int_temp_L)/(2**16)).quantize(Decimal('0.0'))
                int_PM10_H = int.from_bytes(data[15:16], byteorder='big')
                int_PM10_L = int.from_bytes(data[16:17], byteorder='big')
                pm10 = int_PM10_H * 256 + int_PM10_L
                print("温度(0C)", temperature)
                print("湿度(%RH)", humidity)
                print("PM2.5(ug/m3):", pm25)
                print("PM10:", pm10)
                print("甲醛CH2O(ug/m3):", ch2o)
                print("总挥发性有机物TVOC(ug/m3):", tvoc)
                print("二氧化碳CO2(ppm):", co2)
                time.sleep(1)
                refreshlcd = refreshlcd + 1
                if refreshlcd >= 10:
                    refreshlcd = 0
                    # write strings to the buffer
                    # clear the frame buffer
                    frame_black = [0xFF] * int(epd.width * epd.height / 8)
                    #frame_red = [0xFF] * int(epd.width * epd.height / 8)
                    epd.draw_string_at(frame_black, 100, 2, u'PM2.5: ' + str(pm25 )  , font, COLORED)
                    epd.draw_string_at(frame_black, 2, 27, u'温度: ' + str(temperature), font, COLORED)
                    epd.draw_string_at(frame_black, 100, 27, u'湿度: ' + str(humidity) + '%', font, COLORED)
                    epd.draw_string_at(frame_black, 2, 52, u'甲醛: ' + str(ch2o) , font, COLORED)
                    epd.draw_string_at(frame_black, 100, 52, u'PM10:' + str(pm10) , font, COLORED)                    
                    epd.draw_string_at(frame_black, 2, 77, u'TVOC: ' + str(tvoc) , font, COLORED)
                    epd.draw_string_at(frame_black, 100, 77, u'二氧化碳: ' + str(co2) , font, COLORED)
                    # display the frames
                    epd.display_frame(frame_black, frame_red)
    except KeyboardInterrupt:
        if ser != None:
            ser.close()

    if ser != None:
        ser.close()

if __name__ == '__main__':
    main()
