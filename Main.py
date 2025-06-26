import tkinter as tk
import os

os.system("cls")


root = tk.Tk()

list = ['atttack', 'defend', 'run']


frame = tk.Frame(root)
# frame.grid can be anywhere between here and before the label = tk.Label
frame.grid()
for i in range(3):
    frame.rowconfigure(i)
    for j in range(2):
        frame.columnconfigure(j)
        label = tk.Label(master=frame, bg="Blue", text=f"{list[i]}")
        label.grid(row=i, column=j)





root.mainloop()