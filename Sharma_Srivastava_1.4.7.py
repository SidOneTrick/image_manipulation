from __future__ import print_function
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import os.path 
import PIL
import PIL.ImageDraw            

def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = "Images/" # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_picture(original_image, frameloc, items, colorscale = "RGBA"):
    frame = PIL.Image.open(frameloc)
    cross = PIL.Image.open(items)
    width_image, height_image = original_image.size
    width_frame, height_frame = frame.size
    width_cross, height_cross = cross.size
    print (frame.size)
    width_cross = float(width_cross)
    height_cross = float(height_cross)
    print (frameloc)
    if frameloc == "frame/frame1.png":
        if width_frame != width_image and height_frame != height_image:
            frame_resize = frame.resize((width_image, height_image))
            width_frame, height_frame = frame_resize.size
        else:
            pass
    elif frameloc == "frame/frame2.png":
        if width_frame != 1.25 * width_image and height_frame != 1.2*height_image:
            print ("True")
            frame_resize = frame.resize((int(1.5*width_image),int(1.5*height_image)))
            width_frame, height_frame = frame_resize.size
            print (frame_resize.size)
        else:
            pass
    else:
        pass
    
    tp_background = PIL.Image.new("RGBA", (width_frame, height_frame), None)
    width_background, height_background = tp_background.size
    ncrossheight = height_image/3.
    whratio = width_cross/height_cross
    ncrosswidth = int(ncrossheight * whratio)
    cross_resize = cross.resize((ncrosswidth, int(ncrossheight)))
    cross_resize = cross_resize.rotate(30)
    cross_resize = cross_resize.convert("RGBA")
    cross_resize.save("new_cross.png")
    offset = ((width_background - width_image) // 2, (height_background - height_image) // 2)
    original_image.paste(cross_resize, (int(width_image/3.5), height_image - height_image/2), cross_resize)
    tp_background.paste(original_image, offset)
    tp_background.paste(frame_resize, (0, 0), mask = frame_resize)
    frame.save("frame.png")
    tp_background.save("new_image.png")
    return tp_background


def frame_everything(directory = None):
    
    frame = raw_input("What frame would you like?(options: basic, flower): ")
    item = raw_input("What item would you like on your image?(options: cross, football, controller):  ")
    if frame == "basic":
        frame = "frame/frame1.png"
    elif frame == "flower":
        frame = "frame/frame2.png"
        
    if item == "cross":
        item = "Project_Images/cross.png"
    elif item == "controller":
        item = "Project_Images/controller.png"
    elif item == "football":
        item = "Project_Images/football.png"
    if directory == None:
        directory = "Images/" # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
     
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        
        # Round the corners with radius = 30% of short side
        new_image = frame_picture(image_list[n], frame, item)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)