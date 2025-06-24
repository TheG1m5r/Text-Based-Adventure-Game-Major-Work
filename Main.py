import tkinter as tk
import os

os.system("cls")


root = tk.Tk()

list = ['atttack', 'defend', 'run']


frame = tk.Frame(root)
for i in range(len(list)):
    grid = frame.grid(row=i, column=0)
    label = tk.Label(grid, bg="Blue", text=f"{list[i]}")
    label.grid()





root.mainloop()
#deez