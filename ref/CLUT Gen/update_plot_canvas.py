from tkinter import * 
import matplotlib.pyplot as plt 
import numpy as np 
import sys

window = Tk() # the main Tkinter window 
window.title('Plotting in Tkinter') 
window.geometry("1200x800") 

subCanvas = Canvas(window, width=600, height=400, highlightbackground="black", bg="gray80")
subCanvas.pack()
subCanvas.place(x=400, y=200)

gammaVal = DoubleVar() 
gammaVal.set(round(1.0,2))
gamma=2
def exitProgram():
        sys.exit(0)

def plot(): 
    a=1

    x = np.linspace(0, 10*np.pi, 100) 
    gamma=gammaVal.get()
    gamma = gamma +0.1
    gammaVal.set(round(gamma, 2))
    print (gamma)
    y=pow(x, gamma)
    #y = np.sin(x) 

    plt.ion() 
    fig = plt.figure() 
    ax = fig.add_subplot(111)   # 1x1 grid in 1st (quadrant?) subplot
    line1, = ax.plot(x, y, 'b-') # -b blue -r red
    plot1 = fig.add_subplot(221)
    plot1.plot(y)
    fig.canvas.draw() 

    fig.canvas.flush_events() 
    y=pow(x, gamma)
    plot1 = fig.add_subplot(224)
    plot1.plot(y)
    fig.canvas.draw() 
    for phase in np.linspace(0, 10*np.pi, 100): 
	    line1.set_ydata(np.sin(0.5 * x + phase))
    #fig.canvas.draw() 
	#fig.canvas.flush_events() 

class MenuButtons:
    hexColor="white"
    def __init__(iself, master):        # __init__(className, variable)
        iself.plot_button = Button(window, text="Plot", activebackground='red3', bg='red', fg='white', width=10, height=1, command=plot)
        
        iself.plot_button.place(x=30, y=10)
        master.bind('<Escape>', lambda event: exitProgram())
        
# run the gui 
rootButtons = MenuButtons(window)
window.mainloop() 