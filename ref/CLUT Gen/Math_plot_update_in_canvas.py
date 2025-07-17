
# Note this program hangs as proper exit() does not exist
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
from tkinter import *
import numpy as np
import sys

root = Tk()
root.geometry("1200x800") 
gammaFig, ax = plt.subplots(figsize=(4, 2.8), sharey=True)           
# this determines the figure size !!!!!!!!!!!!!!!

label = Label(text = "Matplotlib + Tkinter!")
label.config(font=("Courier", 32))
label.pack()

rootCanvas = Canvas(root, width=300, height=200, bg="green")
rootCanvas.pack()
rootCanvas.place (x=250,y=100) # this size has no effect on subplots as figsize determines figure size

canvas2 = FigureCanvasTkAgg(gammaFig, master=rootCanvas) 
canvas2.get_tk_widget().pack()
#plt.ion()              # automatically updates without explicit commands

gammaVal = DoubleVar() 
gammaVal.set(round(1.0,2))
gamma=2

print (canvas2.get_width_height())

def plotData(): # Plot data on Matplotlib Figure
        plt.clf()       # clear previous plot before updating plot !!!
        x = np.linspace(0, 255, 255)  # start, stop # of evenly spaced samples to generate between start & stop
        xN=x/255 # normalized x value
        gamma=gammaVal.get()
        gamma = gamma +0.1
        gammaVal.set(round(gamma, 2))
        y=pow(xN, gamma)
        plt.plot(x, y)
        plt.axis((0,255,0,1.0))
        #plt.show()      # show plot in separate window
        gammaFig.canvas.draw()

def exitProgram():
        sys.exit(0)
class MenuButtons:
    hexColor="white"
    def __init__(iself, master):        # __init__(className, variable)
        master.bind('<Escape>', lambda event: exitProgram())
        master.bind('p', lambda event: plotData())
        
rootButtons = MenuButtons(root)
root.mainloop()