from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Subplot
import numpy as np
import sys

window = Tk() # the main Tkinter window 
window.title('Plotting in Tkinter') 
window.geometry("1200x800") 

subCanvas = Canvas(window, width=400, height=200, highlightbackground="black", bg="gray80")
subCanvas.pack()
subCanvas.place(x=600, y=200)

# plotting the graph in  
# tkinter window 
def exitProgram():
        sys.exit(0)
        
def plot(): 
  
    # the figure that will contain the plot 
    fig = Figure(figsize = (4, 5), dpi = 100) # the figure that will contain the plot
    fig1=plt.figure()
    ax = Subplot(fig1, 111)  
    #ax = plt.subplots()
    fig1.add_subplot(ax)

    y = [i**2 for i in range(101)] # list of squares 

    plot1 = fig.add_subplot(111)  # adding the subplot 
    fig1.set_figheight(100)

    plot1.plot(y) 
    t = np.arange(0, 2*np.pi, .01)
    ax.plot(t, np.sin(t))
   # canvas.draw()

    canvas = FigureCanvasTkAgg(fig1, master = window)   #Tkinter canvas containing Matplotlib figure
    canvas.draw() 
    canvas.get_tk_widget().pack() 
    #plt.show()

class MenuButtons:
    hexColor="white"
    def __init__(iself, master):        # __init__(className, variable)
        iself.plot_button = Button(window, text="Plot", activebackground='red3', bg='red', fg='white', width=10, height=1, command=plot)
        
        iself.plot_button.place(x=30, y=10)
        master.bind('<Escape>', lambda event: exitProgram())
        
# run the gui 
rootButtons = MenuButtons(window)
window.mainloop() 