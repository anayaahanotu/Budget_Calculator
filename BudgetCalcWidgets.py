from tkinter import *
import tkinter.ttk as ttk
import typing as t
import numpy as np


#algorithm is from outside sources.
#https://www.youtube.com/watch?v=hgysxwqXXM0&t=61s
def hex_to_rgb(hexCode:str) -> tuple[int, int, int]:
    """
    hex_to_rgb(hexCode) -> rgb: tuple[int, int, int]
    hexCode: str: hex code to convert to RGB
    converts hex value to rgb value
    returns tuple[int, int, int]: tuple[int, int, int]: calculated RGB value
    """
    #initialize the RGB value as an emty list
    rgb:list = []

    #create list of all hex values
    hexValues = list("0123456789ABCDEF")

    #get rid of the leading #
    hexCode = hexCode.replace("#", "")

    #each hex code duo represents 1 RGB Value. Convert each duo to a decimal
    #i for index
    for i in range(0, 6, 2):
        #initialise the current hex value
        currentValue = hexCode[i:i+2]
        
        #go through each element in current value using enumerate
        #enumerate -> item (index 1) and index in currentValue (index 0)
        #use the formula: 
        #   16 ^ ((length of hex value) - current index)
        #   * the hexidecimal's decimal equivalent (found based on its index 
        #   in hexValues)
        currentRGB = sum(list(map(
            lambda x: 16 ** (1 - x[0]) * hexValues.index(x[1].upper()),
            enumerate(currentValue)
        )))

        #add the RGB value to the rgb list
        rgb.append(currentRGB)

    
    return tuple(rgb)

def rgb_to_hex(rgb:t.Iterable[int]) -> str:
    """
    rgb_to_hex(rgb: tuple[int, int, int]) -> str
    rgb: tuple[int, int, int]: rgb values to convert to hex
    converts rgb value to hexadecimal value
    returns str: calculated hexadecimal value
    """
    #initialize hex string
    hexCode:str = "#"

    #make sure rgb is 3 values long
    rgb = rgb[:3]

    #use .join() and map() to go through each element in RGB
    #convert RGB to a string value of hex (exclude "0x")
    #then add it to hex code

    hexCode += "".join(
        map(lambda x: "{:02x}".format(x).replace("0x", ""), rgb)
    )

    return hexCode
class Mutable_Label(Label):

    '''Makes a label that can be changed based on the user's desire'''

    def __init__(self, master:Tk|Frame, kwargs:dict[str, str]|None = None,
                 make_numeric:bool=False, focusColor:str = 'lightgrey'):
        '''
        Mutable_Label(self, master, kwargs, make_numeric, focusColor)
        master: Tkinter.Tk, Tkinter.Frame: parent widget of this widget
        kwargs: dict[str, str]: keyword args for Tkinter.Label
        make_numeric: bool: restrict the label to only have numeric values
        focusColor: str: color of the label when pressed
        Returns none
        '''
        Label.__init__(self, master, **kwargs)

        self.atts = kwargs

        if 'bg' in self.atts.keys():
            self.color = self.atts['bg']
        else:
            self.color='white'

        self.is_number_strict = make_numeric

        self['cursor'] = 'xterm'

        self.master.update_idletasks()
        
        #set color based on the focus
        self.bind('<Button>', lambda e: self.focus_set())
        self.bind('<FocusIn>', lambda e: self.configure(bg=focusColor))
        self.bind('<FocusOut>', lambda e: self.configure(bg=self.color))

        #allow the user to update the value when it is in focus
        self.bind('<Key>', self.update_text)

        #set the starting value to 0 if self is numeric
        if self.is_number_strict:
            self["text"] = "0"
        
    def update_text(self, event:Event) -> None:
        '''
        Mutable_Label.update(event)
        event: tk.Event
        Updates the label based on the key
        '''

        #remove last character if backspace
        if event.keysym == 'BackSpace':
                self.configure(text=str(self['text'])[:-1])

                #set 0 as the placeholder value for when there is no value
                #and the label is numberic
                if self["text"] == "" and self.is_number_strict:
                    self["text"] = "0"

        #remove whole text if deleted
        elif 'Delete' in event.keysym:
                self.configure(text='')

                #set 0 as the placeholder value for when there is no value
                #and the label is numberic
                if self["text"] == "" and self.is_number_strict:
                    self["text"] = "0"

        #if the label is supposed to be strictly numeric, only allow the
        elif self.is_number_strict:
            #get rid of the placeholder zero for when there is no value
            if self["text"] == "0":
                self["text"] = ""
            #add values if it is numeric
            if event.char.isnumeric():
                self.configure(text=str(self['text']) + event.char)
            #add the decimal point if it does not exist
            elif event.char == '.':
                if '.' not in self['text']:
                   self.configure(text=str(self['text']) + event.char)
            #add the negative only at the beginning of the number
            elif event.char == '-':
                if self['text'] == '':
                    self.configure(text=str(self['text']) + event.char)

        #else, just add the character
        else:
            self.configure(text=str(self['text']) + event.char)

        self['text'] = self['text']

    def change_base_color(self, color):
        '''
        Mutable_Label.change_base_color(color)
        color: str: color of the widget when not in focus
        Changes the base color of this label
        '''

        self['bg'] = color
        
        self.bind('<FocusOut>', lambda e: self.configure(bg=color))

    def change_focus_color(self, color):
        '''Mutable_Label.change_focus_color(self, color)
        color: str: any valid color
        Changes the focus color of the label'''

        self.bind('<FocusIn>', lambda e: self.configure(bg=color))


class ScrollingFrame(Frame):
    """
    Create a scrollable window
    """
    def __init__(self, master:Tk|Frame, kwargs:dict|None = None,
                    scrollAxis:str = "X"):
        """
        ScrollingFrame(self, master, kwargs, scrollReigon)
        master: tkinter.Tk|tkinter.Frame: parent widget ScrollingFrame
        kwargs: dict: keyword arguments for tkinter.Frame
        scrollAxis: str: axis on which to scroll:
            - 'X': scroll along x-axis
            - 'Y': scroll along y-axis
            - "XY": scroll along x-axis and y-axis

        creates an instantiation of ScrollingFrame
        """
        #method from https://www.youtube.com/watch?v=0WafQCaok6g

        #instantiate self
        Frame.__init__(self, master, **kwargs)

        #initialize scrollAxis, scrollCanvas, and scrollBars
        self.scrollAxis:str = scrollAxis.upper()
        self.scrollCanvas:Canvas = Canvas(self, bg=self["bg"])
        #initialize length of scrollbars to be the same as the number of axis
        #to scroll through
        self.scrollbars:np.ndarray[ttk.Scrollbar] = np.full((len(scrollAxis)),
                                                            None
                                                    )

        #declare contentFrame to hold the content
        self.contentFrame:Frame

        #if Y axis is chosen, create a vertical scrolling bar
        if 'Y' in scrollAxis:
            #pack the scrollCanvas to the left side of self
            self.scrollCanvas.pack(side=LEFT, fill=BOTH, expand=1)
            #initialize a vertical scrollbar
            self.scrollbars[0] = ttk.Scrollbar(
                self, 
                orient="vertical",
                command=self.scrollCanvas.yview,
            )
            self.scrollbars[0].pack(side=RIGHT, fill="y")

            #configure the canvas to be connected to the scrollbar
            self.scrollCanvas.configure(yscrollcommand=self.scrollbars[0].set)


    def change_scroll_axis(direection:str) -> None:
        """
        ScrollingFrame.change_scroll_axis(direction)
        direction: str: axis on which to scroll:
            - 'X': scroll along x-axis
            - 'Y': scroll along y-axis
            - "XY": scroll along x-axis and y-axis
        
        """
        pass
    
    @property
    def contentFrame(self) -> Frame:
        pass
    def update_scrollbar(self) -> None:
        pass
    def setFocus(self, e) -> None:
        pass
    def removeFocus(self, e) -> None:
        pass