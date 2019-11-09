#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
from PIL import Image, ImageDraw
import zipfile
import configparser
#Takes a card coordinate (R6.B22) and converts it to an x,y coordinate (51,11)
def coord2xy(coord):
    assert coord[2]=='.'
    if coord[0] in 'sS':
        y=8
    elif coord[0] in 'rR':
        y=17
    else:
        raise "Row prefix must be [RS]"
    y-=int(coord[1])
    if coord[3] in 'aA':
        x=0
    elif coord[3] in 'bB':
        x=39
    else:
        raise "Column prefix must be [AB]"
    if coord[4] in 'aA':
        x=30
    elif coord[4] in 'bB':
        x=38
    else:
        x+=int(coord[4])*5
        x+=int(coord[5])
    return x,y

#Clears a punch (card coordinates)
def clearbit(coord):
    global bits
    x,y=coord2xy(coord)
    print("Clearing",x,y)   
    bits[y][x]=False

#Sets a punch (card coordinates)
def setbit(coord):
    global bits
    x,y=coord2xy(coord)
    print("Setting",x,y)    
    bits[y][x]=True


bits=[[False for x in range(69)] for y in range(18)]

#Set the punches here
for bit in [    'R0.A14','R0.A22','R0.A31','R0.A33','R0.A44','R0.A50','R0.A51',
                'R1.A00','R1.A03','R1.A12','R1.A13','R1.A14','R1.A17','R1.A31','R1.A33','R1.A44','R1.A50',
            'R6.A53',
        'S1.A14',
        'S2.A00','S2.A10','S2.A22',
        'S3.A00','S3.A20',
        'S7.A00','S7.A02',
        'S8.A00','S8.A30','S8.A40','S8.A54']:
    setbit(bit)

for bit in [    'R0.B03','R0.B04','R0.B11','R0.B13','R0.B20','R0.B21','R0.B33','R0.B34','R0.B40','R0.B42','R0.B50','R0.B54',
                'R5.B53',
            'R6.B22','R6.B30',
        'R7.B22','R7.B30',
        'S0.B00',
        'S7.B12','S7.B13',
        'S8.B00','S8.B01','S8.B10','S8.B11','S8.A54']:
    setbit(bit)

#Got some good good ascii art
sys.stdout.write('+'+('—'*69)+'+\n')
for y in range(18):
    sys.stdout.write('|')
    for x in range(69): #nice
        if x==31 or x==37:
            sys.stdout.write('|')
        elif x>31 and x<37:
            sys.stdout.write(' ')
        else:
            sys.stdout.write('#' if bits[y][x] else '·')
    sys.stdout.write('|\n')
sys.stdout.write('+'+('—'*69)+'+\n')

with zipfile.ZipFile('cardpack.zip') as cardpack:
    f_im=Image.open(cardpack.open('front.png'))
    b_im=Image.open(cardpack.open('back.png'))
    with cardpack.open('offsets.txt') as offsets:
        config=configparser.ConfigParser()
        config.read_string(offsets.read().decode('ASCII'))
        print(config.sections())
        f_origin_x=float(config['Front']['originX'])
        f_origin_y=float(config['Front']['originY'])
        f_offset_x=float(config['Front']['offsetX'])
        f_offset_y=float(config['Front']['offsetY'])
        b_origin_x=float(config['Back' ]['originX'])
        b_origin_y=float(config['Back' ]['originY'])
        b_offset_x=float(config['Back' ]['offsetX'])
        b_offset_y=float(config['Back' ]['offsetY'])
    

    #Render the PNGs
    f_draw = ImageDraw.Draw(f_im)
    b_draw = ImageDraw.Draw(b_im)
    for xidx in range(69):
        for yidx in range(18):
            if xidx>30 and xidx<38: continue
            #Don't tell Professor Mead, these numbers are magic
            f_xcen=f_origin_x+(xidx*f_offset_x)
            f_ycen=f_origin_y+(yidx*f_offset_y)
            b_xcen=b_origin_x+(xidx*b_offset_x)
            b_ycen=b_origin_y+(yidx*b_offset_y)
            #It's hole-punchin' time
            if bits[yidx][xidx]:
                f_draw.ellipse([(f_xcen-10,f_ycen-10),(f_xcen+10,f_ycen+10)],'black','black')
                b_draw.ellipse([(b_xcen-10,b_ycen-10),(b_xcen+10,b_ycen+10)],'black','black')
    f_im.save("front.png")
    b_im.save("back.png")
