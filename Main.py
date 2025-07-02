import tkinter as tk
import os

os.system("cls")

# selected button
selbutton = 0


def up_input(event):
    global selbutton
    if selbutton > 0:
        selbutton -= 1
    print(selbutton)

def down_input(event):
    global selbutton
    if selbutton < 100:
        selbutton += 1
    print(selbutton)

def test():
    while True:
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
        root.update() # update pastes it into the ui interface without the need of root.mainloop, otherwise the root.mainloop will only run once and the while loop with output nothing
        frame.destroy() # deletes the frame so that it can reopen with the correct selected box


root = tk.Tk()
root.bind("<w>", up_input)
root.bind("<s>", down_input)





test()





root.mainloop()