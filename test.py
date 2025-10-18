import tkinter as tk

import BudgetCalcWidgets as tk2

import numpy as np

root = tk.Tk()
root["bg"] = "pink"
root.geometry("500x500")

myParams:dict = {
    "master" : root,
    "kwargs": {"bg":"red", "font":("Georgia", 20), "borderwidth":3, 
               "relief":tk.GROOVE, "width":7, "height":2},
    "make_numeric":True,
    "focusColor": "orange"
}

myWidgets:np.ndarray[tk.Label] = np.full((5, 5), None)



for i in range(5):
    for j in range(5):
        myWidgets[i][j] = tk2.Mutable_Label(**myParams)
        myWidgets[i][j].grid(row=i, column=j)

root.update()
root.update_idletasks()

print(myWidgets[0][0].winfo_width())






root.mainloop()
print(1)

