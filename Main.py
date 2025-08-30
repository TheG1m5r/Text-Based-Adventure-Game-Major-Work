from tkinter import *
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from pygame import mixer
import random
import os

os.system("cls")

# selected button
selbutton = 0


def up_input(event):
    global selbutton # idk why i need so many globals for one thing but i can't be bothered rn to try to fix it if it works well
    if selbutton > 0:
        selbutton -= 1
    print(selbutton) # for testing purposes

def down_input(event):
    global selbutton
    if selbutton < 100:
        selbutton += 1
    print(selbutton)

def left_input(event):
    pass

def right_input(event):
    pass

def space_input(event):
    pass

def soundTest(event):
    mixer.init()
    mixer.Sound("jewjewjew.mp3").play() # appoligies for bad 

def test():
    list = ['attack', 'defend', 'run']
    frame = tk.Frame(root)
    # frame.grid can be anywhere between here and before the label = tk.Label
    frame.grid()
    for i in range(3):
        frame.rowconfigure(i)
        for j in range(2):
            BG="Blue"
            frame.columnconfigure(j)
            if i == selbutton:
                BG="Red"
            label = tk.Label(master=frame, bg=BG, text=f"{list[i]}")
            label.grid(row=i, column=j)
    
def locationScreen(areaName, areaImage, areaDesc):
    # chance for enemy encounter + the enemy that gets encountered
    if random.randint(0,1) < 2:
        random.choice(("test", "ligma"))
    
    # area name
    areaFont = Font(family="Times New Roman", size=int(root.winfo_screenheight()*0.024), weight="bold", underline=1) # creates a custom font that maybe used where ever
    labelAreaName = tk.Label(text=areaName, fg="black", anchor="center", font=areaFont)
    labelAreaName.columnconfigure(0)
    
    # area image
    img = Image.open(areaImage) # opens the image as original size
    img = img.resize((int(root.winfo_screenwidth()*0.75), int(root.winfo_screenheight()*0.5)), Image.LANCZOS) # resizes image to acomidate window size   ## also didn't need the use of PILLOW as i ended up using percentages which tkinter already handles...   ### also don't understand LANCZOS or what it is
    img = ImageTk.PhotoImage(img)
    imageLabel = tk.Label(root, image=img)
    imageLabel.image = img # keeps the reference alive otherwise tkinter will garbage-collect it, otherwise image will not appear when ran

    # area description
    descFont = Font(family="Arial", size=12)
    labelAreaDesc = tk.Label(text=areaDesc, font=descFont, wraplength=int(root.winfo_screenwidth()*0.65))

    # area options
    ## get code from test data once it actually works

    # packing the screen elements onto the tab
    labelAreaName.pack()
    imageLabel.pack()
    labelAreaDesc.pack()

    test()



root = tk.Tk()
root.state("zoomed") # maximises the window to "fullscreen"

# button binds
root.bind("<w>", up_input)
root.bind("<s>", down_input)
root.bind("<a>", left_input)
root.bind("<d>", right_input)

root.bind("<space>", space_input)

root.bind("<f>", soundTest)

## resize screen bind? for if the player wants the screen bigger or larger -- not important rn


# grid for entire window that enables resizeability of window
## make sure to actually do this
for i in range(3):
    for j in range(3):
        pass
##

#test()
testDesc = "Tall trees rise around you, their dense canopy blotting out much of the sky. Shafts of light pierce through the leaves, illuminating patches of moss and tangled roots. The air is cool and damp, carrying the earthy scent of soil and distant foliage. Every sound—whether a birdcall or the snap of a twig—seems to echo deeper than it should."
locationScreen("Forest_1", "forest_1.png", testDesc) # images must be png otherwise need Pillow import to change that but idk how to, and don't feel like trying so ima manually change to png




root.mainloop()