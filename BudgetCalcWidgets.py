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
        #16 ^ ((length of hex value) - current index)
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
                    scrollAxis:str = "Y"):
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
        self.scrollbars:np.ndarray[ttk.Scrollbar] = np.full(
            (2),
            None
        )
        self.change_scroll_axis(self.scrollAxis)

        self.scrollCanvas.bind(
            "<Configure>", 
            lambda e: self.scrollCanvas.configure(
                scrollregion=self.scrollCanvas.bbox("all")
            )
        )

        #this frame holds the contents of the scrolling bar
        self.displayFrame:Frame = Frame(self.scrollCanvas, bg=self["bg"])

        self.scrollCanvas.create_window(
            (0, 0), 
            window=self.displayFrame, 
            anchor = "nw"
        )

        import random

        self.scrollCanvas.bind(
            "<Enter>",
            lambda e: [
                self.scrollCanvas.focus_set(), 
                self.scrollCanvas.bind_all(
                    "<MouseWheel>",
                    self.on_mouse_wheel,
                    "+"
                )
            ]     
        )

        self.scrollCanvas.bind(
            "<Leave>",
            lambda e: self.scrollCanvas.unbind_all("<MouseWheel>"),
            "+"
        )

        self.update_scrollbar()

    def on_mouse_wheel(self, e:Event):
        """
        ScrollingFrame.on_mouse_wheel(e)
        e: Tkinter.Event
        Scrolls the canvas: vertically if there is a vertical scrollbar.
        horizontally if the scrollbar is only horizontal
        """

        # method from: 
        # https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar

        if self.scrollAxis == "X":
            self.scrollCanvas.xview_scroll(e.delta, "units")

        elif "Y" in self.scrollAxis:
            self.scrollCanvas.yview_scroll(-1 * e.delta, "units")
            self.update_idletasks()

    def change_scroll_axis(self, direction:str) -> None:
        """
        ScrollingFrame.change_scroll_axis(direction)
        direction: str: axis on which to scroll:
            - 'X': scroll along x-axis
            - 'Y': scroll along y-axis
            - "XY": scroll along x-axis and y-axis
        
        """

        self.scrollAxis = direction.upper()

        #destroy existing scrollbars
        if self.scrollbars[0]: self.scrollbars[0].destroy()
        if self.scrollbars[1]: self.scrollbars[1].destroy()

        #if Y axis is chosen, create a vertical scrolling bar
        if 'Y' == self.scrollAxis:

            self.scrollbars[0] = ttk.Scrollbar(
                self, 
                orient="vertical",
                command=self.scrollCanvas.yview,
            )
            self.scrollbars[0].pack(side=RIGHT, fill="y")

            #configure the canvas to be connected to the scrollbar
            self.scrollCanvas.configure(yscrollcommand=self.scrollbars[0].set)
            self.scrollCanvas.pack(side=LEFT, fill=BOTH, expand=1)

        #else if X axis is chosen, create a vertical scrolling bar
        elif 'X' == self.scrollAxis:
            
            self.scrollbars[0] = ttk.Scrollbar(
                self, 
                orient="horizontal",
                command=self.scrollCanvas.xview,
            )
            self.scrollbars[0].pack(side=BOTTOM, fill="x")
            self.scrollCanvas.pack(side=TOP, fill=BOTH, expand=1)

            self.scrollCanvas.configure(xscrollcommand=self.scrollbars[0].set)

        #else if X and Y axis is chosen, create a horizontal and vertical
        #scrolling bar
        elif self.scrollAxis == 'XY':
            #initialize a vertical scrollbar
            self.scrollbars[0] = ttk.Scrollbar(
                self, 
                orient="vertical",
                command=self.scrollCanvas.yview,
            )
            self.scrollbars[0].pack(side=RIGHT, fill="y")

            #configure the canvas to be connected to the scrollbar
            self.scrollCanvas.configure(yscrollcommand=self.scrollbars[0].set)


            #initialize a vertical scrollbar
            self.scrollbars[1] = ttk.Scrollbar(
                self, 
                orient="horizontal",
                command=self.scrollCanvas.xview,
            )
            self.scrollbars[1].pack(side=BOTTOM, fill="x")

            #configure the canvas to be connected to the scrollbar
            self.scrollCanvas.configure(xscrollcommand=self.scrollbars[1].set)

            self.scrollCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    
    def update_scrollbar(self) -> None:
        """
        ScrollingFrame.update_scrollbar()
        Updates the contents and attributes of the canvas to Tkinter and the
        Frame 
        """
        self.update()


        self.scrollCanvas.configure(scrollregion=self.scrollCanvas.bbox("all"))

        self.update()

    def add_item(self, obj, 
            args:tuple|None = None, 
            kwargs:dict|None = None,
            row:int = 0,
            column:int = 0
    ) -> object:
        """
        ScrollingFrame.add_item(self, obj, args, kwargs, row, column)
        obj: Tkinter widget: class type object to put into the scrollFrame
        args: tuple: list of arguments for the object
        kwargs: list of keyword arguments for the object
        row: int: grid row number to place the element
        column: int: grid column number to place the object

        returns the item added to the dataframe
        WHEN DELETING THE OBJECT, CALL update_scrollbar()
        """


        if not args: args = ()
        if not kwargs: kwargs = {}
        
        newObject = obj(self.displayFrame, *args, **kwargs)

        newObject.grid(row=row, column=column)

        self.update_scrollbar()

        #returns the object so that the programmer can modify/delete the object
        #later
        return newObject

    

def main():
    import random
    import numpy as np

    root = Tk()
    root.geometry("500x500")
    root["bg"] = rgb_to_hex(
        (
            random.randrange(127, 256),
            random.randrange(127, 256),
            random.randrange(127, 256)
        )
    )

    scrollFrame:ScrollingFrame = ScrollingFrame(
        root,
        kwargs={"bg":root["bg"]}, 
        scrollAxis="XY"
    )

    scrollFrame.place(x=0, y=0, relwidth = 0.25, relheight=1)


    arrayOfLabels = np.full((50, 5), None)

    for i in range(50):
        for j in range(5):
            arrayOfLabels[i][j] = scrollFrame.add_item(
                obj=Label,
                kwargs={
                    "bg":"white", 
                    "fg":"black", 
                    "font": ("Georgia", 12),
                    "width":10, 
                    "height":5,
                    "text":f"Button {random.randrange(1, 3000)}"
                },
                row = i, 
                column= j
            )

    print(1)




    root.mainloop()

if __name__ == "__main__":
    main()

class DataList (Frame):
    pass