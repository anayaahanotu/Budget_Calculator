from tkinter import *

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