# -*- coding: utf-8 -*-

"""
Anaya Ahanotu
Tue Jul 18 18:34:30 2023
Brings all parts of calculator into one body.
Also saves + retrieves data to & from the computer
"""
#import needed modules
import tkinter as tk
import time
import sys
import pickle
import numpy as np
import pandas as pd

#import the different parts of the program
import BudgetCalcWidgets as bcw


#create the window
root = tk.Tk()
root.geometry('1200x800') #set size of window
root['bg'] = '#f9afc0' #makes for a soft, neutral pink background
root.title('Budget Calculator')



class Budget_Calculator(tk.Frame):
    '''Budget_Calculator
    makes the GUI budget calculator'''
    
    def __init__(self, master) -> None:
        """Budget_Calculator(self, master, kwargs)
        master: tkinter.Tk
        Initiates the budget_calculator
        """
        #set up frame
        tk.Frame.__init__(self, master, bg=master['bg'],) 
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.master.update()
        self.master.update_idletasks()

        if "#" not in self["bg"]:
            self.color:tuple = bcw.rgb_to_hex(tuple(map(
                lambda x: x // 256, root.winfo_rgb(self["bg"])
            )))
        else:
            self.color = self["bg"]
        

        #title of project
        title:tk.Label = tk.Label( 
            root,
            bg=root['bg'],
            fg='white',
            text='Budget Calculator',
            font=('Sauber Script', 30, 'bold'),
        )

        #set relative position of all the widgets, instead of a fixed position

        title.place(
            relx=0.5,
            rely=0, relwidth=0.5,
            relheight=0.05,
            anchor='n'
            ) 

        #give selected and unselected tabs two distinct colors
        #selected tabs are a few shaeds darker than unselected tabs

        #save unselected color as RGB and hex, same with selected Color
        self.__unselectedColor:list = [bcw.hex_to_rgb(self.color), self.color]
        self.selectedColor = [
             list(value - 50 for value in self.__unselectedColor[0]),           
        ]

        for index, value in enumerate(self.selectedColor[0]):
            if value < 0:
                self.selectedColor[0][index] = 0

        self.selectedColor[0] = tuple(self.selectedColor[0])

        self.selectedColor.append(bcw.rgb_to_hex(self.selectedColor[0]))


        self.__MODES:list[str] = [
            'income and expenses',
            'savings',
            'analysis',
            'investments',
            'taxes'
            ] #keep track of all possible modes
        
        self.selectedMode:str = self.__MODES[0] #know what mode you are in


        #keep the tabs in a narrow frame about right next to each other

        tabFrame:tk.Frame = tk.Frame(self, bg=self.color)


        tabFrame.place(relx=0, rely=0.08, relwidth=1) 

        # set a tab for each of the modes
        # store it to an empty dictionary
        tabs:dict[str, tk.Label] = {}

        # go through each element in the tabs
        # add the corresponding tab to the app

        for index, label in enumerate(self.__MODES):
            tabs[label] = tk.Label(
                tabFrame,
                font=("Georgia", 24),
                fg="White",
                bg= self.__unselectedColor[1],
                text=label.capitalize(),
            )

            #place the label
            tabs[label].grid(row=0, column=index, ipadx=2)

            #allow the label to change mode of window
            tabs[label].bind("<Button>", lambda e: self.__set_mode(index))



        #allow people to save their data
        self.saveButton:tk.Label = tk.Label( 
            self,
            text='Save',
            font=('Georgia', 18, 'bold'),
            bg = '#2BAF6A',
            fg = 'white',
            relief='raised'
        )

        self.saveButton.place(
            relx=1,
            rely=0,
            relwidth=0.06,
            relheight=0.05,
            anchor='ne'
        )
        

        self.window:tk.Frame = tk.Frame(
            self,
            bg=self.selectedColor[1]
        )

        #allow the program gather up to date info on placement of tabs

        self.master.update_idletasks() 

         #figure out where the main window should begin

        starty:float = (float(tabFrame.place_info()['rely']) 
                        + float(tabFrame.winfo_height()/self.winfo_height()))

        #above code allows for less messy placement of the window
        self.window.place(
            relx=0,
            rely=starty,
            relwidth=1,
            relheight=1-starty
            ) 

        #set up the frames that display the data
        
        self.incomeFrame = None 
        self.incomeAnalysisFrame = None
        self.spendingsFrame = None
        self.investmentsFrame = None
        self.taxesFrame = None

        self.CurrentModeIndex:int|None = None #set default mode
        self.__set_mode(0)
        self.revive_data() # get data previously saved

        #we put this last to make sure users do not accidentally save unused data

        self.saveButton.bind('<Button>', self.save_data) 

        #keep the frame up to date on the placement of all the widgets

        self.master.update()

    def __set_mode(self, value):
        pass 
    def save_data(self):
        pass
    def revive_data(self):
        pass

 

if __name__ == "__main__":
    a = Budget_Calculator(root)

    root.mainloop() #show the window

