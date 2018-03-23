from __future__ import print_function
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import os.path 
import PIL
import PIL.ImageDraw            


def grayout(pic):
    pic = PIL.Image.open(pic).convert("L")
    
    pic.save("grey.png")