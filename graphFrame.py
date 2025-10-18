"""
Anaya Ahaontu
18 June 2025
Creates the graphs to display on the budget calculator
"""

#import needed modules
import random
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import math
import datetime
from datetime import datetime as dt 
import typing as t
from enum import Enum


#declare charts enum
class Charts(Enum):
    BAR_CHART = "BAR CHART"
    LINE_PLOT = "LINE PLOT"
    SCATTER_PLOT = "SCATTER PLOT"
    PIE_CHART = "PIE CHART"



#declare the graphing class
class Graphing(tk.Frame):
    '''
    Make a Frame to display different graphs
    During the initial instantiation, there will be a warning that a chart is
    not created. This is because a chart has not been selected yet. 
    '''

    #give the list of charts (referenced later in code)
    __CHARTS = tuple(item.value for item in Charts)
    
    def __init__(self, master:tk.Frame|tk.Tk, **kwargs):
        '''GraphFrame(args, kwargs):\n
            master: Tkinter.Frame() or Tkinter.Tk()\n
            **kwargs: tkinter.Canvas parameters -- NOT 'bg'
        '''

        #make sure bg is not added twice
        if "bg" not in kwargs: kwargs["bg"] = "white" 

        #initialize self
        tk.Canvas.__init__(self, master, **kwargs) 

        # assign where independant, dependant
        # and graph attributes will be stored
        self.xData:np.ndarray = []
        self.yData:np.ndarray[int|float] = []
        self.__graphAtts:dict = {}

         #initialize the type
        self.type:Charts = Charts

        #allow graphs to change size with window size
        self.bind(
            "<Configure>", 
            lambda e: self.__create_graph(newDates=False), 
            "+"
            )
        
        print("Ignore the following error: ", end="")
        
    def get_graph_atts(self) -> dict:
        return self.__graphAtts

    def switch_graph(self, graphType:str) -> None:
        '''
        GraphFrame.switch_graph(graphType)\n
        graphType: str: any enum value for Charts\n
            - "BAR CHART"\n
            - "LINE PLOT"\n
            - "SCATTER PLOT"\n
            - "PIE CHART"\n
            input is not case sensitive\n

        creates a chart
        '''

        #check if developer made proper option
        # if so, update self.type and create the graph 
        if graphType.upper() in self.__CHARTS:
            self.type = Charts(graphType.upper())

             #draw the graph
            self.__create_graph()

        #else, warn the programmer that an invalid option was selected
        else:
            print(f"ERROR: Invalid argument for switch_graph. "
                  + f"You selected: '{graphType}'. "
                  + "Graph was not updated.\n"
                  + f"Please choose any: {self.__CHARTS}")

    def update_data(
            self,
            independant:t.Iterable[t.Any]=None,
            dependant:t.Iterable[int|float]=None,
            **kwargs
            ):
        """
        GraphFrame.set_attributes(): None

        independant: iterable: list of all x values\n
            dates must be in MM/DD/YYYY format! \n
        dependent: iterable: list of all y values\n
        xName: str: x-axis label\n
        yName: str: y-axis label\n
        title: str: title of the graph\n
        xAreDates: bool: treat x values as dates\n
        treatAsText: bool: treat x values as plain text\n
        timespan: str: num_iterations.unit_of_time | all\n
            'W' -> Week\n
            'M' -> Month\n
            'Y' -> year\n
            'all' -> all time\n
        pointSize: int: size of the point\n
        pointColor: str: pointColor\n
        makeHistogram: bool: make the bar chart as a histogram\n
        numBins: int: number of bins\n
        fillColor: str|iterable[str]: color(s) to fill bar chart\n
        lineWidth: int: size of line for line chart\n
        lineColor: str: color of chart line\n

        Used with all charts: xName, yName, title\n

        Unique to scatterplot: xAreDates, treatAsText, timespan, pointSize,
        pointColor\n

        Unique to line graph: xAreDates, treatAsText, timespan, pointSize,
        pointColor, lineWidth, lineColor\n

        unique to bar chart: makeHistorgram, fillColor, numBins\n

        sets up the attributes for the chart and draws the graph
        """

        #update the data
        self.__graphAtts.update(kwargs)

        #if there is new x data, then update x data
        if independant:
            self.xData = np.array(independant)
        
        #if there is new y data, update the y data
        if dependant:
            self.yData = np.array(dependant)

        self.__create_graph(newDates=False)
    
    def set_attributes(
            self, independant:t.Iterable[t.Any] = (), 
            dependant:t.Iterable[int|float] = (),
            *, xName:str = '', yName:str = '', title:str = '',
            xAreDates:bool = False, treatAsText:bool = False, timespan:str = 'all',
            pointSize:int = 10, pointColor:str = 'black', makeHistogram:bool = False,
            numBins:int = 10, fillColor:str|t.Iterable[str] = "black",
            lineWidth:int = 5, lineColor:str = "black",
            ) -> None:
        
        """
        GraphFrame.set_attributes(): None

        independant: iterable: list of all x values\n
            dates must be in MM/DD/YYYY format! \n
        dependent: iterable: list of all y values\n
        xName: str: x-axis label\n
        yName: str: y-axis label\n
        title: str: title of the graph\n
        xAreDates: bool: treat x values as dates\n
        treatAsText: bool: treat x values as plain text\n
        timespan: str: num_iterations.unit_of_time | all\n
            'W' -> Week\n
            'M' -> Month\n
            'Y' -> year\n
            'all' -> all time\n
        pointSize: int: size of the point\n
        pointColor: str: pointColor\n
        makeHistogram: bool: make the bar chart as a histogram\n
        numBins: int: number of bins\n
        fillColor: str|iterable[str]: color(s) to fill bar chart/pie chart\n
            - must be interable[str] for custom colors for pie chart \n
        lineWidth: int: size of line for line chart\n
        lineColor: str: color of chart line\n

        Used with all charts: xName, yName, title\n

        Unique to scatterplot: xAreDates, treatAsText, timespan, pointSize,
        pointColor\n

        Unique to line graph: xAreDates, treatAsText, timespan, pointSize,
        pointColor, lineWidth, lineColor\n

        unique to bar chart: makeHistorgram, fillColor, numBins\n

        sets up the attributes for the chart and draws the graph
        """
        # set self.xValues passed independant values
        # and self.yValues to  and dependant values
        self.xData, self.yData = np.array(independant), np.array(dependant)

        #update self.__graphAtts to be all attributes except the first two items
        self.__graphAtts = dict(locals())
        del self.__graphAtts["independant"]
        del self.__graphAtts["dependant"]

        #draw the graph
        self.__create_graph()



    def __create_graph(self, newDates = True) -> None:
        '''GraphFrame.create_graph(graphType)\n
        independant: seq: x-axis values\n
        dependant: seq: numeric: y-axis values\n
        newDates: bool: new dates entered (default True)
        '''

        #make sure we don't end up with multiple charts in one frame
        for widget in self.winfo_children(): 
            widget.destroy()

        # draw the graph that corresponds to the current chart selected
        match self.type:
            case Charts.BAR_CHART:
                self.__make_bar_graph()
            case Charts.LINE_PLOT:
                self.__make_line_chart(formatDates=newDates)
            case Charts.SCATTER_PLOT:
                self.__make_scatterplot(formatDates=newDates)
            case Charts.PIE_CHART:
                self.__make_pie_chart
            #if no valid option is used, warn the programmer
            case _:
                print(f"ERROR: invalid bar type: {self.type}. Chart not created") 
           
    def __reset_plot(self) -> None:
        """
        Graph.__reset_plot(self, plotWidth, plotHeight, dpiRef) -> None
        Resets the fig and axis
        """
        #update window to get most accurate window size
        self.update_idletasks()
        self.master.update_idletasks()

        #store the length, width, and average of length and width.
        #the plot will reference these measurements to determine plot size
        plotWidth = self.winfo_width()
        plotHeight = self.winfo_height()
        dpiRef = min(plotHeight, plotWidth)

        #create a figure if it does not already exist
        if not hasattr(self, "fig") or self.fig is None:
            #initialize the figure
            self.fig = plt.figure()
    
        # remove current axis from memory.
        if hasattr(self, "ax"):
            del self.ax

        # clear the figure and create a new axis
        self.fig.clear()

        #create the axis where the chart will be made
        self.ax = self.fig.add_subplot(111)

        #resize fig
        self.fig.set_size_inches(plotWidth//120, plotHeight//110)
        self.fig.set_dpi(dpiRef/8)
        #ABOVE ARE THE DIMENSIONS NEEDED TO ENSURE CHART FITS IN THE WINDOW.

        #put the scatterplot on the frame
        self.graph = FigureCanvasTkAgg(self.fig, self)
        chart = self.graph.get_tk_widget()
        chart.configure(width=plotWidth, height=plotHeight, bg=self["bg"])
        chart.pack()
            
    def __make_scatterplot(self, formatDates:bool) -> None:
        '''
        GraphFrame.make_scaterplot(self, formatDates): void\n
        formatDates: bool: does we have new dates to update\n

        displays a scatterplot
        '''

        self.update_idletasks()
        self.master.update_idletasks()

        #make sure reference dict is not empty
        #if it is, then it means the window just opened without any data
        # and nothing should be plotted
        if self.__graphAtts != {}:
            #remove rows with no values
            self.__clean_data()

            #if the data is text: convert to string
            #allows matplotlib to interpret data as as text, not numeric
            if self.__graphAtts["treatAsText"]:
                self.xData = self.xData.astype(str)

            #else if the data are dates, convert to datetime
            elif self.__graphAtts["xAreDates"]:

                #if the dates need to be formatted, then we got new dates
                #update dates
                if formatDates:
                    #convert all days to datetime to work with them easier
                    # filter them to be within specified timeframe
                    # the user wants
                    self.__filter_dates()

            #reset the matplotlib plot -- remove current one from memory.
            #create new blank slate
            self.__reset_plot()

            #reduce clutter of x axis
            self.fig.autofmt_xdate()

            #graph the scatter plot
            self.ax.scatter(
                self.xData,
                self.yData,
                s=self.__graphAtts["pointSize"],
                color=self.__graphAtts["pointColor"]
                )
            
            #set axis labels
            self.ax.title.set_text(self.__graphAtts["title"])
            self.ax.set_xlabel(self.__graphAtts["xName"])
            self.ax.set_ylabel(self.__graphAtts["yName"])
            
            #draw the chart
            self.graph.draw()

            #update the window
            self.update_idletasks()
            self.master.update_idletasks()

    def __make_bar_graph(self) -> None:
        """
        GraphFrame.__make_bar_graph(self): void\n

        displays a bar graph
        """

        #update window
        self.update_idletasks()

        #if __graphAtts is not empty, there is data to be plotted
        #create the bar chart
        if self.__graphAtts != {}:

            #clean data
            self.__clean_data()

            #reset plot -- clear the current plot from memory
            self.__reset_plot()

            #clean up x axis
            self.fig.autofmt_xdate()
            
            #if the user wants a histogram: make the histogram
            if self.__graphAtts["makeHistogram"]:

                # create the histogram
                n, bins, patches = self.ax.hist(
                        self.xData,
                        linewidth=self.__graphAtts["lineWidth"],
                        edgecolor=self.__graphAtts["lineColor"],
                        bins = self.__graphAtts["numBins"]
                        )

                #make the colors

                #if the user included a list of colors,
                #iterate through each color and assign to bar graph

                #create own flag variables 
                # or else if statement will get long and confusing
                isSeq = isinstance(self.__graphAtts["fillColor"], t.Iterable)
                isNotStr = not isinstance(self.__graphAtts["fillColor"], str)
                isListOfStrs = all(map(
                    lambda value: isinstance(value, str) == True,
                    self.__graphAtts["fillColor"]
                    ))

                #now check the conditions
                if (isSeq and isNotStr and isListOfStrs):
                    # if user inputted less colors than there are
                    # bins, iterate through user inputted colors
                    # and add it to a new list of colors until they are the 
                    #same length
                    if len(self.__graphAtts["fillColor"]) < len(patches):
                        
                        #index of __graphAtts to reference
                        index = 0

                        # add the user inputted colors to colors
                        colors = list(self.__graphAtts["fillColor"])

                        #add new color if there are less colors than bars
                        while len(colors) < len(patches):
                            #add a new color
                            colors.append(self.__graphAtts["fillColor"][index])

                            #if index is at the last index of the list of
                            #user inputted colors, reset index to 0
                            if index == len(self.__graphAtts["fillColor"]) - 1:
                                index = 0
                            #else, add 1 to index
                            else:
                                index += 1

                    #else if there are more colors than bars, cut off the 
                    #excess colors and assign to a new list
                    elif len(self.__graphAtts["fillColor"]) < len(patches):
                        colors = self.__graphAtts[:len(patches)]
                    
                    #else assign the fill color to a new list
                    else:
                        colors = list(self.__graphAtts["fillColor"])
                    
                    #loop through the each bar and each color in colors

                    for color, bar in zip(colors, patches):
                        bar.set_facecolor(color)

                #else, set the facecolor to one color
                else:
                    for bar in patches:
                        bar.set_facecolor(self.__graphAtts["fillColor"])


            #else; they want a normal bar graph
            else:
                # draw the bar graph
                self.ax.bar(
                    self.xData,
                    self.yData,
                    color=self.__graphAtts["fillColor"],
                    linewidth=self.__graphAtts["lineWidth"],
                    edgecolor=self.__graphAtts["lineColor"]
                    )

            #set the title, xLabel, yLabel, bar color, and outline thickness
            self.ax.title.set_text(self.__graphAtts["title"])
            self.ax.title.set_text(self.__graphAtts["title"])
            self.ax.set_xlabel(self.__graphAtts["xName"])
            self.ax.set_ylabel(self.__graphAtts["yName"])


            #update the window
            self.update_idletasks()


    def __make_line_chart(self, formatDates: bool) -> None:
        '''
        GraphFrame.make_line_chart(self, formatDates): void\n
        formatDates: bool: does we have new dates to update\n

        displays a scatterplot
        '''

        self.update_idletasks()
        self.master.update_idletasks()

        #make sure reference dict is not empty
        #if it is, then it means the window just opened without any data
        # and nothing should be plotted
        if self.__graphAtts != {}:
            #remove rows with no values
            self.__clean_data()

            #if the data is text: convert to string
            #allows matplotlib to interpret data as as text, not numeric
            if self.__graphAtts["treatAsText"]:
                self.xData = self.xData.astype(str)

            #else if the data are dates, convert to datetime
            elif self.__graphAtts["xAreDates"]:

                #if the dates need to be formatted, then we got new dates
                #update dates
                if formatDates:
                    #convert all days to datetime to work with them easier
                    # filter them to be within specified timeframe
                    # the user wants
                    self.__filter_dates()

            #reset the matplotlib plot -- remove current one from memory.
            #create new blank slate
            self.__reset_plot()

            #reduce clutter of x axis
            self.fig.autofmt_xdate()

            #graph the scatter plot
            self.ax.plot(
                self.xData,
                self.yData,
                color=self.__graphAtts["lineColor"]
                )
            
            #set axis labels
            self.ax.title.set_text(self.__graphAtts["title"])
            self.ax.set_xlabel(self.__graphAtts["xName"])
            self.ax.set_ylabel(self.__graphAtts["yName"])
            
            #draw the chart
            self.graph.draw()

            #update the window
            self.update_idletasks()
            self.master.update_idletasks()

    def __make_pie_chart(self, e = None):
        """
        GraphFrame.__make_pie_chart(self)
        creates a plot of a pie chart
        """

        #update the window
        self.update_idletasks()
        self.master.update_idletasks()

        #if __graphAtts is not an empty dictionary, there is data to process
        # graph the pie chart
        if self.__graphAtts != {}:
            #reset plot
            self.__reset_plot()

            #clean data
            self.__clean_data()

            #if the user inputted a list, color the pie chart based on
            # developer input.
            if (isinstance(self.__graphAtts["fillColor"], t.Iterable)
                and not isinstance(self.__graphAtts["fillColor"], str)):

                # initialize variable to create a copy of dev inputted colors
                colors = list(self.__graphAtts["fillColor"])

                #if there are less colors than pie slices: add random colors 
                #until there are the same amount of colors and pie slices
                if len(colors) < len(self.xData):
                    #while length of colors < num pie slices: add new color
                    while len(colors) < len(self.xData):
                        #generate a random color
                        newColor = ("#" + "".join(
                            random.choice("ABCDEF1234567890") 
                            for i in range(6)
                            ))
                        
                        #add random color to the list of colors
                        colors.append(newColor)

                #else if there are more colors than number of slices: reduce
                #list of colors length
                elif len(colors) > len(self.xData):
                    # cut off the excess colors from the list of colors
                    colors = colors[:len(self.xData)]

                #draw the pie chart
                patches, text, autotexts = self.ax.pie(
                    self.yData,
                    labels=self.xData,
                    colors=colors,
                    autopct="%1.1f%%"
                )

            #else; dev did not input custom color list:
            else:
                # draw the pie chart without user inputted data
                patches, text, autotexts = self.ax.pie(
                    self.yData,
                    labels=self.xData,
                    autopct="%1.1f%%"
                )

            #set font to readable size
            for label, pctLabels in zip(text, autotexts):
                    label.set_fontsize(16.0)
                    pctLabels.set_fontsize(14.0)
                    
    def __filter_dates(self):
        """
        GraphFrame.__filter_dates(self)
        filters the dates to be in desired time frame
        """

        # convert the current xData to datetime
        self.__convert_to_datetime()

        #check to see if user wants all time; if not, filter by timespan
        if self.__graphAtts['timespan'].lower() != "all":
            #get the desired timeframe
            timeFrame = self.__graphAtts["timespan"].split(".")

            #cast the M/W/Y noatation to uppercase
            #reduces case sensitivity
            timeFrame[1] = timeFrame[1].upper()

            #make sure the xData and yData are within the range specified.

            #put self.xValues and self.yValyes in temporary dataFrame to 
            #make sure the xvalues and yvalues are sorted along side each
            #other and data does not get mixed up
            tempData = pd.DataFrame(
                {"date": self.xData, "value": self.yData},
            )

            #sort the dataFrame by date in descending order
            tempData = tempData.sort_values(
                "date",
                ascending=False,
                ignore_index=True
                )
            

            #cast timeFrame[0] to int; this is the number of iterations of
            # the unit of time
            timeFrame[0] = int(timeFrame[0])

            #if timeFrame[1] == "W", filter by num weeks
            if timeFrame[1] == "W":
                # have the earliest date be timeSpan[0] * 7 days before
                #most recent date
                timeSubtract = datetime.timedelta(timeFrame[0] * 7)
                beginningDate = tempData.date[0] - timeSubtract

            #else if timeSpan[1] == "M", filter by num months
            elif timeFrame[1] == "M":
                # have beginning date be 
                #(int value timeSpan[0] * 30.44 days) before most recent date
                timeSubtract = datetime.timedelta(int(timeFrame[0] * 30.44))
                beginningDate = tempData.date[0] - timeSubtract

            #else if timeSpan[1] == "Y", filter by num years
            elif timeFrame[1] == "Y":
                # have the beginning date be
                #(int value of timeSpan[0] * 365.25 days) before most recent date
                timeSubtract = datetime.timedelta(int(timeFrame[0] * 365.25))
                beginningDate = tempData.date[0] - timeSubtract

            # filter the dataframe and remove all rows that are less than
            #specified beginning date
            tempData = tempData[tempData.date >= beginningDate]

            #reassign self.xValues and self.yValues based on dataframe
            self.xData = tempData.date
            self.yData = tempData.value

            #delete temporary dataframe from memory
            del tempData
         
    def __convert_to_datetime(self) -> None:
        '''
        GraphFrame.convert_to_datetime(dates)\n
        converts x-axis dates to datetime format\n
        '''
        #store the dates in a new format and save it to variable
        tempIndependant = []
        for element in self.xData:
            #split it into a list so we can work with each unit at a time
            element = element.split("/")

            for unit in range(2):
                #make sure the month and day are in MM and DD format
                element[unit] = element[unit].zfill(2)
            
            #make sure year is in YYYY format
            element[2] = element[2].zfill(4)

            #put the properly formatted months and dates into a new string
            tempDate = "{}/{}/{}".format(*element)

            #set the format for the dates
            format = "%m/%d/%Y"

            #make the newdate in datetime format
            newDate = dt.strptime(tempDate, format)

            #add it to the list of dates
            tempIndependant.append(newDate.date())
        
        #update stored independant values to be in datetime format
        self.xData = tempIndependant

    def close(self) -> None:
        """
        self.close(self)\n
        closes the window
        """
        #close the plot
        if hasattr(self, "fig"):
            self.fig.clear()
            del self.fig
        
        if hasattr(self, "ax"):
            self.ax.clear()
            del self.ax
        
        #destory the frame
        self.destroy()

    def __clean_data(self) -> None:
        '''
        GraphFrame.clean_data(independant, dependant)\n
        cleans the data by filtering out None types and null\n
        reassigns self.xData and self.yData to be the cleaned data
        '''

        #if the plot is not supposed to be a histogram
        #filter the x and y axis  
        if not self.__graphAtts["makeHistogram"]:

            #make sure xData and yData are the same length
            #set the max length of both sequences to be the smallest length
            maxLength = min(len(self.xData), len(self.yData))

            #slice both sequences to go up to the length of the smaller list
            self.xData = self.xData[:maxLength]
            self.yData = self.yData[:maxLength]

            #save data to dataframe
            data = pd.DataFrame({'x': self.xData, 'y': self.yData})

            #drop all rows with no values
            data = data.dropna()

            #declare the cleaned data to xData and yData
            self.xData = data.x
            self.yData = data.y
        
        #if it is supposed to be a histogram, look at only x values
        else:
            data = pd.DataFrame({'x': self.xData})

            #drop all rows with no values
            data = data.dropna()

            #declare the cleaned data to xData and yData
            self.xData = data.x

        del data 

def main():
    import random
    root = tk.Tk()

    root.geometry("500x500")

    x = np.arange(-10, 10, 0.01)

    y = []

    phi = (1 + math.sqrt(5)) / 2

    for a in x:
        try:
            value = a**2 + math.sin(a)

            if (-50 <= value <= 50):
                y.append(value)
            else:
                y.append(None)
                
        except Exception:
            y.append(None)

    chart:Graphing = Graphing(root)
    
    chart.pack(fill=tk.BOTH, expand=True)

    color = "#" + "".join(random.choice("ABCDEF1234567890") for i in range(6))

    chart.set_attributes(
        independant=x,
        dependant=y,
        xName="WTF",
        yName="WTH",
        pointColor=color,
        title="NOOOOOOOO"
    )

    chart.switch_graph("SCATTER PLOT")


    root.mainloop()




if __name__ == "__main__":
    main()