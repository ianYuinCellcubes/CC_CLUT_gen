from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

def grafik(uebergebene_daten=(10, 10, 10, 10)):
    global canvas1

    if canvas1:
        canvas1.get_tk_widget().destroy()
    
    datenplot = uebergebene_daten

    fig = Figure(figsize=(10, 4), dpi=100)
    plot1 = fig.add_subplot(111) 

    canvas1 = FigureCanvasTkAgg(fig, master = window)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=TOP, fill=NONE, expand=0)
    window.after(1000, None)


window = Tk() 

canvas1 = None

# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("700x700") 


# button that displays the plot 
plot_button = Button(master = window, command = grafik, height = 2, width = 10, text = "Plot") 
# place the button 
plot_button.pack() 

# run the gui 
window.mainloop()