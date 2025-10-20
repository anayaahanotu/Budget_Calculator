import tkinter as tk
from tkinter import colorchooser
import BudgetCalcWidgets as tk2
import numpy as np
import random

root = tk.Tk()
root["bg"] = "#c4eb7f"
root.geometry("500x500")

scrollBar = tk2.ScrollingFrame(
    root,
    kwargs={"bg":"orange"},
    scrollAxis="Y"
)

scrollBar.place(relx=0, rely=0, relwidth=1, relheight=0.5, anchor=tk.NW)

root.mainloop()
print(1)



