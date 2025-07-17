# ******************************************************************
#
#   SLM response curve data acquisition & CLUT file generation 
#                       M. Jin 2024.09
#      
#
# ******************************************************************

from tkinter import *   # Button, Frame, Tk
from tkinter import ttk
from screeninfo import get_monitors     # pip install screeninfo in command line first
import sys
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from scipy.interpolate import CubicSpline
import numpy as np
import time
import datetime
from PIL import ImageTk, Image # pip install pillow
import pathlib
#from datetime import date

cPath=pathlib.Path(__file__).parent.resolve()   # current script directory

i=0
sWidth=[0,0]
sHeight=[0,0]
for monitor in get_monitors():
    sWidth[i] = monitor.width
    sHeight[i] = monitor.height
    print(i, str(sWidth[i]) + 'x' + str(sHeight[i]))
    i+=1
screenWidth=sWidth[1]
screenHeight=sHeight[1]

#cDay= datetime.date.today()
cTime= datetime.datetime.now()
#cTime= date.today()
#d1= cDay.strftime("%m%d%y")
d2= cTime.strftime("%m%d%y_%H%M")
print ("Time: ", d2)
root = Tk()
#logoImage = PhotoImage(file='C:\C3_logos\C3Logo1.png')
#root.iconphoto(False, logoImage)
root.title("CLUT Gen")
x=sWidth[0]-1000            # offset within screen size
y=400                         # offset within screen size
screenAspect=sWidth[0]/sHeight[0]
screenN=2.5
# menu screen size scaling factor (min 2, max 4 for full screen)
menuWidth=int(sWidth[0]*screenN/4)      # menu window width/height
menuHeight=int(sHeight[0]*screenN/4)
print("WxH ", menuWidth, menuHeight)
menuWidth=1920; menuHeight=1200
xOffset=sWidth[0]-menuWidth-20      # sWidth[0]-menuWidth-20
yOffset=+10    # offset within monitor size
root.geometry(str(menuWidth)+"x"+str(menuHeight)+"+"+str(xOffset)+"+"+str(yOffset))

subWidth=screenWidth/10; subHeight=screenHeight/10
canvasWidth=int(menuWidth*0.35); canvasHeight=int(menuWidth*0.35/screenAspect) # make this screenN*1/10 of target screen size for simple scaling
winWidth=int(canvasWidth*0.5); winHeight=int(canvasHeight*0.5)
canOffsetX=int(canvasWidth/2); canOffsetY=int(canvasHeight/2)
tableWidth=int(menuWidth*0.25); tableHeight=int(menuWidth*0.7/screenAspect)

#  ***************** Menu Screen Canvases *****************
rootCanvas = Canvas(root, width=canvasWidth, height=canvasHeight, highlightbackground="black", bg="gray80")
rootCanvas.pack()   # Top Right Canvas 
rootCanvas2 = Canvas(root, width=canvasWidth, height=canvasHeight, highlightbackground="black", bg="gray80")
rootCanvas2.pack()  # Bottom Right Canvas
rootTable = Canvas(root, width=tableWidth, height=tableHeight, highlightbackground="black", bg="gray80")
rootTable.pack()  # Bottom Right Canvas
smallCanvas = Canvas(root, width=winWidth, height=winHeight, highlightbackground="black", bg="gray90")
# canvase size overriden by gammaFig, ax = plt.subplots(figsize=(4, 2.8), sharey=True)  
smallCanvas.pack()  # Bottom Left Gamma Canvas 

canvasX=menuWidth-canvasWidth-20; canvasY=50    # offset within subwindow
tableX=menuWidth-canvasWidth-tableWidth-225; tableY=75    # offset within subwindow
rootCanvas.place(x=canvasX, y=canvasY)
canvas2Top=canvasY+canvasHeight+70   # Canvas2 Top (y)
rootCanvas2.place(x=canvasX, y=canvas2Top)
rootTable.place(x=tableX, y=tableY)
#sCanBottom=canvas2Top + canvasHeight - winHeight
sCanBottom=725
smallCanvas.place(x=10, y=sCanBottom)

# *******************************************************
figWidth=menuWidth*0.4; figHeight=figWidth*3/4
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
print(menuWidth); print(plt.rcParams['figure.dpi'])
dataFig, bx = plt.subplots(figsize=(4,2.5), sharey=True)    # this determines the figure size !!!!!!!!!!!!!!!
gammaFig, ax = plt.subplots(figsize=(3,2), sharey=True)   # figsize= (600*px, 400*px) for inches conversion          
rtCanvas2 = FigureCanvasTkAgg(dataFig, master=rootCanvas2) 
rtCanvas2.get_tk_widget().pack()
sCanvas2 = FigureCanvasTkAgg(gammaFig, master=smallCanvas) 
sCanvas2.get_tk_widget().pack()
# *******************************************************

line = rootCanvas.create_line(2, 2,canvasWidth, 2,fill='black')
line = rootCanvas.create_line(2, canvasHeight, canvasWidth, canvasHeight,fill='black')
line = rootCanvas.create_line(2, 2, 2, canvasHeight,fill='black')
line = rootCanvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight,fill='black')
#root.geometry("800x480+"+str(x)+"+"+str(y))
win1 = Toplevel()
win1.geometry(f"{sWidth[1]}x{sHeight[1]}+{sWidth[0]}+000") # <- shift window right by sWidth[0] of main monitor
win1.overrideredirect(True)
root.focus_set()        # Ensures root window has focus to operate without mouse-click select

counter = IntVar(value=127)
gammaVal = DoubleVar()          # for decimal place textvariable=gammaVal
gammaVal.set(round(2.2, 2))    #  gamma 2.2 => 22
plt.axis((0,255,0,1.0))
gamma=1 # replaced by gammaVal.get()

gIncrement= IntVar(value=16)
colorSelect = 7  # initialize global variable 1(B) 2(G) 4(R) 7(W)
clutBits=10  # 10 or 12 bits
gammaBits=8
gammaN=2**gammaBits #256
clutN = 2**clutBits
dataRowM=17; dataColN=4
dataN=0
initFlag=IntVar(value=0)
dataList = []; grayLevel = []
blueData = []; greenData = []; redData = []
tableCol0=[]; tableCol1=[]; tableCol2=[]; tableCol3=[]  # grid pointers for Entry()
splineArray = [[]*1 for i in range(clutN)]
clutArray = []  # clut[2**clutBits][4]
cs=[]; cs1=[]; cs2=[]; xs=[]  # 2^clutBits spline array for each color

# *********** Tab Menu Controls ***************



# ************** Functions & Classes ******************
def exitProgram():
        sys.exit(0)
    
def load_file():
    global nRow, nCol
    global dataN, cPath
    print("load")
    #os.chdir("C:\\CLUTS") # \\ for literal '\' in the string !!!!!!!!
    dataList=[] # !!! need to reset lists to avoid array overflow !!!
    grayLevel.clear(); redData.clear(); greenData.clear(); blueData.clear()
    file = str(cPath) + "\\Data\\Measured_Data.csv"    
    dataList = load_data (file)   # \\ for literal '\' in the string !!!!!!!
    dataN=len(dataList) # of data in csv file
    #print(len(dataList))  
    for i in range(0, dataN):
        grayLevel.append(float(dataList[i][0]))
        redData.append(float(dataList[i][1]))
        greenData.append(float(dataList[i][2]))
        blueData.append(float(dataList[i][3]))
    
    nRow = len(dataList)
    nCol = len(dataList[0])
    #print(dataList)
    update_SLM_data(dataList, nRow, nCol)
    spline()
    # Note. dataList array values may not be available globally after read
    
def appendList(l,element):
    for i in range(len(element)):
        l[i].append(element[i])
    return l

def spline():
    #dataFig.clear()
    global splineArray, blueData, greenData, redData
    splineArray = [[]*1 for i in range(clutN)]
    temp=[]; temp1=[]; temp2=[]
    cs = CubicSpline(grayLevel, blueData)
    cs1 = CubicSpline(grayLevel, greenData)
    cs2 = CubicSpline(grayLevel, redData)
    xSpacing=256/(clutN)    # 2 to the n-th power
    #print(xSpacing, "sp"); print (grayLevel); print (blueData)
    xs = np.arange(0,256, xSpacing)
    for i in range (0,clutN):
        temp.append(cs(xs[i]).item())
        temp1.append(cs1(xs[i]).item())
        temp2.append(cs2(xs[i]).item())
    splineArray = appendList(splineArray, temp)     #  b adds list as additiona 'column' each time appendList is executed
    splineArray = appendList(splineArray, temp1)    #  g adds list as additiona 'column' each time appendList is executed
    splineArray = appendList(splineArray, temp2)    #  r adds list as additiona 'column' each time appendList is executed
    
    bx.plot(grayLevel, blueData, '+', label='data')
    bx.plot(grayLevel, greenData, '+', label='data')
    bx.plot(grayLevel, redData, '+', label='data')
    bx.plot(xs, temp, color='blue', label='B')
    bx.plot(xs, temp1, color='green', label='G')
    bx.plot(xs, temp2, color='red', label='R')

    xticks=np.arange (0,255.1,50)
    bx.set_xticks(xticks)
    dataFig.canvas.draw()
    print("L: ", len(temp))
    #print (splineArray)
    #print(temp)
    print("Red Spline")
    
def load_data(filename):
    mylist =[]
    f = open (filename, 'r')    # 'r' for read
    csvReader = csv.reader(f, delimiter=',')
    for row in csvReader:
        mylist.append(row)
    return mylist

def store_data():
    concatData=[grayLevel, redData, greenData, blueData]
    listData = list(map(list, zip(*concatData)))    # transpose concatData *** very important !!!! ***
    filename=str(cPath) +"\\Data\\Measured_Data2.csv" # overwrites existing file
    f = open (filename, 'w', newline='')    # 'w' for write; newline='' needed to avoid insertion of blank line between rows
    csvWriter = csv.writer(f)
    csvWriter.writerows(listData)
    f.close()  

def update_SLM_data(grayData, dataRowM, dataColN):  # Data Table Update after file load
    global tableCol0, tableCol1, tableCol2, tableCol3
    tableCol0=[]; tableCol1=[]; tableCol2=[]; tableCol3=[]
    if (len(tableCol0)<(dataN+1)):
        appendGridEntry(grayData, dataRowM, dataColN)

def appendGridEntry(grayData, dataRowM, dataColN):
    for i in range(dataRowM):
        for j in range(dataColN):
            tableData = Entry(rootTable, width=8, fg='blue', font=('Arial',10), justify='center')
            tableData.grid(row=i, column=j)         # add empty slot to the visible table
            if (j==0):
                roundData = (grayData[i][j])
            else:
                roundData = round(float(grayData[i][j]), 4)
                
            tableData.insert(END, roundData)   # fill slot with grayData[][]
            if j==0:
                tableCol0.append(tableData)        # this is pointer info, not value
            if j==1:
                tableCol1.append(tableData)        # this is pointer info, not value
            if j==2:
                tableCol2.append(tableData)        # this is pointer info, not value
            if j==3:
                tableCol3.append(tableData)        # this is pointer info, not value
    #print("Length", len(tableCol0))

def updateSplineGraph():
    bx.cla()                # clear existing data plot
    dataFig.canvas.draw()   # update Figrure
    #time.sleep(1)
    spline()


def readTable():
    global grayLevel, redData, greenData, blueData
    grayLevel = []; redData =[]; greenData =[]; blueData=[]
    temp0=[]; temp1=[]; temp2=[]; temp3=[]
    temp0=[tableData.get() for tableData in tableCol0]
    temp1=[tableData.get() for tableData in tableCol1]
    temp2=[tableData.get() for tableData in tableCol2]
    temp3=[tableData.get() for tableData in tableCol3]
    grayLevel = [float(string) for string in temp0]
    redData = [float(string) for string in temp1]
    greenData = [float(string) for string in temp2]
    blueData = [float(string) for string in temp3]

    
def updateSpline(): # read table entries & update graph
    
    readTable()
    #print(grayLevel); print ("red", redData); print ("Green", greenData); print ("Blue", blueData)
    updateSplineGraph()
    
def init_SLM_data():  # Data Table Update
    for i in range(dataRowM):
        for j in range(dataColN):
            tableData = Entry(rootTable, width=8, fg='blue', font=('Arial',10))
            tableData.grid(row=i, column=j)

def clearData():  # Data Table Update
    bx.cla()                # clear existing data plot
    dataFig.canvas.draw() 
    #init_SLM_data()
    #updateSplineGraph()
    
def rgb2hex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def displayUpdate():
    grayN = counter.get()
    r=int(colorSelect/4)
    g=int(colorSelect/2)-2*r
    b=colorSelect-4*r-2*g
    global hexColor
    hexColor=rgb2hex(r*grayN, g*grayN, b*grayN)
    if grayN<200 or colorSelect==1:
        textColor="white"
    else:
        textColor="black"

    win1.configure(background=hexColor) # set the colour to the next colour generated rootCanvas
    rootCanvas.configure(background=hexColor)
    rootButtons.gLevel.configure(bg=hexColor)
    rootButtons.gLevel.configure(fg=textColor)


def autoMeasure():  # timer based auto grayscale (RGB) change + data acquisition
    global colorSelect
    global counter
    global hexColor
    print ("color1 Change")
    colorSelect=2
    grayN = counter.get()
    r=int(colorSelect/4)
    g=int(colorSelect/2)-2*r
    b=colorSelect-4*r-2*g
    hexColor=rgb2hex(r*grayN, g*grayN, b*grayN)
    if grayN<200 or colorSelect==1:
        textColor="white"
    else:
        textColor="black"
    win1.configure(background=hexColor) # set the colour to the next colour generated rootCanvas
    rootCanvas.configure(background=hexColor)
    rootButtons.gLevel.configure(bg=hexColor)
    rootButtons.gLevel.configure(fg=textColor)
    time.sleep(2)
    print ("color2 Change")
    colorSelect=4
    grayN = counter.get()
    r=int(colorSelect/4)
    g=int(colorSelect/2)-2*r
    b=colorSelect-4*r-2*g
    hexColor=rgb2hex(r*grayN, g*grayN, b*grayN)
    if grayN<200 or colorSelect==1:
        textColor="white"
    else:
        textColor="black"
    win1.configure(background=hexColor) # set the colour to the next colour generated rootCanvas
    rootCanvas.configure(background=hexColor)
    rootButtons.gLevel.configure(bg=hexColor)
    rootButtons.gLevel.configure(fg=textColor)
    time.sleep(5)
    print ("done")

def gammaFigUpdate():
    ax.cla()  # clear previous plot before updating plot !!!
    x = np.linspace(0, 255, 256)  # start, stop # of evenly spaced samples to generate between start & stop
    xN=x/255 # normalized x value
    gamma=gammaVal.get()
    y=pow(xN, gamma)
    ax.plot(x, y)
    ax.axis((0,255,0,1.0))
    xticks=np.arange (0,255.1,50)
    ax.set_xticks(xticks)
    gammaFig.canvas.draw() # associated with smallCanvas by line 77 canvas2 = FigureCanvasTkAgg(gammaFig, master=smallCanvas)

def appendList(l,element):
    for i in range(len(element)):
        l[i].append(element[i])
    return l

def generate_CLUT():
    global splineArray
    nColor=['blue','green', 'red']
    #print (splineArray)
    x = np.linspace(0, 255, 256)
    xN=x/255 # normalized x value
    gamma=gammaVal.get()
    y=xN**gamma     # same as pow(xN, gamma)
    clutArray = [[]*1 for i in range(gammaN)] #  2D array !!!!! mList =[[]]*gammN does not work the same !!!!!
    
    for color in range(0,3):    # just RGB gray assumed to be 0 - 255
       # temp=[]
        temp=[]
        tempList=[] # To simulate 3 columnrow/column data
        tN=[]
        clutColor=nColor[color]
        for i in range (0, 1024):
            temp.append(splineArray[i][color])
        minIndex=temp.index(min(temp))
        maxIndex=temp.index(max(temp))
        slmTruncated=temp[minIndex:maxIndex]
        print("min/max: ", minIndex, maxIndex) 
        print (len(slmTruncated))
        for k in range(0, gammaN):
            searchVal=y[k]
            difference_array = np.absolute(slmTruncated-searchVal) # form absolute difference array to find min difference
            index = difference_array.argmin()                       # min difference == searched index
            nIndex=index.item() + minIndex
            tempList.append(nIndex) # clut index array
            tN.append(nIndex/clutN) # normalized CLUT data to be plotted
        bx.plot(x, tN, color=clutColor)
        clutArray=appendList(clutArray, tempList) # CLUT data to be stored
    print(clutArray)
    dataFig.canvas.draw()
    #bx.plot(x, temp, color='blue')
    #bx.plot(x, temp1, color='green')
    #bx.plot(x, temp2, color='red')
    
def onClickInc(event=None):
    gIncrement.set(int((gIncrement.get())*2))
    if gIncrement.get()>256:
        gIncrement.set(1)
        
def onClickDec(event=None):
    gIncrement.set(int((gIncrement.get())/2))
    if gIncrement.get()<1:
        gIncrement.set(256)
        
def onGammaInc(event=None):
    gammaVal.set(round((gammaVal.get()+0.1),2)) # round(2.2, 2)
    if gammaVal.get()>4:
        gammaVal.set(round(4.0,2))
    gammaFigUpdate()
    
def onGammaDec(event=None):
    gammaVal.set(round((gammaVal.get()-0.1),2))
    if gammaVal.get()<0.1:
        gammaVal.set(round(0.1,2))
    gammaFigUpdate()

def onGammaLinear(event=None):
    gammaVal.set(1.0)
    gammaFigUpdate()
        
def onClickUp(event=None):
    if counter.get()==0 and gIncrement.get()>1:
        counter.set(counter.get()+(gIncrement.get()-1))
    else:
        counter.set(counter.get()+gIncrement.get())
    if counter.get()>255:
        counter.set(0)
    displayUpdate()
    
def onClickDown(event=None):
    if counter.get()>0 and counter.get()<gIncrement.get():
        counter.set(counter.get()-(gIncrement.get()-1))
    else:
        counter.set(counter.get()-gIncrement.get())
    if counter.get()<0:
        counter.set(255)
    displayUpdate()

class MenuButtons:
    hexColor="white"
    def __init__(iself, master):        # __init__(className, variable)
        iself.redButton = Button(root,text="Red", activebackground='red3', bg='red', fg='white', width=8, height=1, command=iself.rStart)
        iself.greenButton = Button(root,text="Green", activebackground='green', bg='green3', fg='white', width=8, height=1, command=iself.gStart)
        iself.blueButton = Button(root,text="Blue", activebackground='blue4', bg='blue', fg='white', width=8, height=1, command=iself.bStart)
        iself.whiteButton = Button(root,text="White",activebackground='gray80', bg='white', fg='black', width=8, height=1, command=iself.wStart)       
        iself.upButton = Button(root,text="Up",activebackground='gray64', bg='gray80', fg='black', width=5, height=1, command=onClickUp) 
        iself.gLevel = Label(root, textvariable=counter, height=2, border=0, relief="solid", anchor="e", justify="center", 
                            bg="gray", fg="white", font=('Arial', 14))
        iself.downButton = Button(root,text="Down",activebackground='gray64', bg='gray80', fg='black', width=5, height=1, command=onClickDown) 
        iself.incLabel = Label(root, text="Increment", width=8, height=1, justify="center")
        iself.keyIndex = Label(root, text="Press: R, G, B, W, Up, Down, Left, Right, Esc", width=40, height=1, justify="left")
        
        iself.grayNLabel = Label(root, text="Gray", width=8, height=1, justify="center")
        iself.redLabel = Label(root, text="Red", width=8, height=1, justify="center")
        iself.greenLabel = Label(root, text="Green", width=8, height=1, justify="center")
        iself.blueLabel = Label(root, text="Blue", width=8, height=1, justify="center")
        
        iself.plusButton = Button(root,text="+",activebackground='gray64', bg='gray80', fg='black', width=3, height=1, command=onClickInc) 
        iself.deltaGray = Label(root, textvariable=gIncrement, width=5, height=1, justify="center")
        iself.minusButton = Button(root,text="-",activebackground='gray64', bg='gray80', fg='black', width=3, height=1, command=onClickDec) 
        
        iself.clutLabel = Label(root, text="CLUT Depth :", justify="left")
        iself.CLUT10 = Button(root,text="10 bit", activebackground='gray64', bg='green4', fg='black', width=12, height=1, command=iself.bit10)
        iself.CLUT12 = Button(root,text="12 bit", activebackground='gray64', bg='gray80', fg='black', width=12, height=1, command=iself.bit12)
        
        iself.measSLM = Button(root,text="Measure SLM",activebackground='gray64', bg='gray80', fg='black', width=12, height=1, command=iself.autoMeasure1)
        iself.storeSLM = Button(root,text="Store Data",activebackground='gray64', bg='gray80', fg='black', width=10, height=1, command=store_data)
        iself.readSLMdata = Button(root,text="Read Data",activebackground='gray64', bg='gray80', fg='black', width=10, height=1, command=load_file)
        iself.genCLUT = Button(root,text="Generate CLUT",activebackground='gray64', bg='gray80', fg='black', width=12, height=1, command=generate_CLUT)
        iself.storeCLUT = Button(root,text="Store CLUT",activebackground='gray64', bg='gray80', fg='black', width=10, height=1, command=iself.wStart)
        iself.recallCLUT = Button(root,text="Recall CLUT",activebackground='gray64', bg='gray80', fg='black', width=10, height=1, command=iself.wStart)
        
        iself.clearButton = Button(root,text="Clear Data",activebackground='gray64', bg='gray80', fg='black', width=10, height=1, command=clearData)
        iself.updateButton = Button(root,text="Update Curve",activebackground='gray64', bg='gray80', fg='black', width=12, height=1, command=updateSpline)
        
        iself.gammaLabel = Label(root, text="CLUT Gamma", width=16, height=1, justify="center", font=('Arial', 11))
        iself.gammaUp = Button(root,text="+",activebackground='gray64', bg='gray80', fg='black', width=3, height=1, command=onGammaInc) 
        iself.gammaValue = Label(root, textvariable=gammaVal, width=4, height=1, justify="right",font=('Arial', 10))
        iself.gammaDown = Button(root,text="-",activebackground='gray64', bg='gray80', fg='black', width=3, height=1, command=onGammaDec) 
        iself.gammaLinear = Button(root,text="Linear",activebackground='gray64', bg='gray80', fg='black', height=1, command=onGammaLinear)
        
        
        dy=60; dx0= 120; dx=50; dx1=200; dx2=65; dy2=60
        y0=90
        x1=15; x2=200
        y1=70; y2=y1+200; y3= y2+dy2*5.5
        bWidth=80; bHeight=40; bHeight1=30
        iself.redButton.place(x=10, y=y0, width=bWidth, height=bHeight1)
        iself.greenButton.place(x=10+dx0, y=y0, width=bWidth, height=bHeight1)
        iself.blueButton.place(x=10+dx0*2, y=y0, width=bWidth, height=bHeight1)
        iself.whiteButton.place(x=10+dx0*3, y=y0, width=bWidth, height=bHeight1)
        iself.upButton.place(x=50, y=y1+dy, width=bWidth, height=bHeight)
        #iself.gLevel.place(x=int(canvasWidth/2)+canvasX-20, y=int(canvasHeight/2)+canvasY-30)
        iself.gLevel.place(x=menuWidth-250, y=150)
        iself.downButton.place(x=50, y=y1+dy*2, width=bWidth, height=bHeight)
        iself.incLabel.place(x=x2+20, y=y1+dy*2.25)
        iself.plusButton.place(x=x2+dx*2+20, y=y1+dy*1.5, width=40, height=bHeight)
        iself.deltaGray.place(x=x2+dx, y=y1+dy*1.5, height=bHeight)
        iself.minusButton.place(x=x2, y=y1+dy*1.5, width=40, height=bHeight)
        iself.keyIndex.place(x=0, y=50)
        
        cWidth=16*8; cOffset=0 ; cY=30
        iself.grayNLabel.place(x=tableX+cOffset, y=cY)
        iself.redLabel.place(x=tableX+cOffset+cWidth, y=cY)
        iself.greenLabel.place(x=tableX+cOffset+cWidth*2, y=cY)
        iself.blueLabel.place(x=tableX+cOffset+cWidth*3, y=cY)
        
        iself.clutLabel.place(x=10, y=y1+dy*3.5, width=160, height=bHeight)
        iself.CLUT10.place(x=200, y=y1+dy*3.5, width=80, height=bHeight)
        iself.CLUT12.place(x=200+bWidth, y=y1+dy*3.5, width=80, height=bHeight)
        
        iself.measSLM.place(x=20, y=y2+dy2*1, height=bHeight)
        iself.storeSLM.place(x = 20+dx1, y=y2+dy2*1, height=bHeight)
        iself.clearButton.place(x = 200+dx1, y=y2+dy2*1.5, height=bHeight)
        iself.updateButton.place(x = tableX+cOffset+cWidth*1.5, y=y3+dy2+50, height=bHeight)
        iself.readSLMdata.place(x = 20+dx1, y=y2+dy2*2, height=bHeight)
        
        iself.genCLUT.place(x=20, y=y2+dy2*3.5, height=bHeight)
        iself.storeCLUT.place(x = 20+dx1, y=y2+dy2*3.5, height=bHeight)
        iself.recallCLUT.place(x=20+dx1, y=y2+dy2*4.5, height=bHeight)
        
        iself.gammaLabel.place(x=x1+dx2*2-10, y=y3+15, height=bHeight)
        iself.gammaUp.place(x = x1+dx2*3, y=y3+dy2, height=bHeight)
        iself.gammaValue.place(x=x1+dx2*2-10, y=y3+dy2, height=bHeight)
        iself.gammaDown.place(x=x1+dx2*1, y=y3+dy2, height=bHeight)
        iself.gammaLinear.place(x=x1+dx2*5, y=y3+dy2, height=bHeight)
        
        master.bind('r', lambda event: iself.rStart()) # bind the key to lambda function since pressed key value is not used (discarded)
        master.bind('g', lambda event: iself.gStart())
        master.bind('b', lambda event: iself.bStart())
        master.bind('w', lambda event: iself.wStart())
        master.bind('<Right>', lambda event: onClickInc())
        master.bind('<Left>', lambda event: onClickDec())
        master.bind('<Up>', lambda event: onClickUp())
        master.bind('<Down>', lambda event: onClickDown())
        master.bind('<Escape>', lambda event: exitProgram())
        
    def rStart(iself):  #alternate: def rStart(iself, _event=None):   # _event=None to prevent warnings
        global colorSelect
        colorSelect=4
        displayUpdate()

    def gStart(iself):
        global colorSelect
        colorSelect=2
        displayUpdate()

    def bStart(iself):
        global colorSelect
        colorSelect=1
        displayUpdate()

    def wStart(iself):
        global colorSelect
        colorSelect=7
        displayUpdate()    
    
    def autoMeasure1(iself):
        global colorSelect
        colorSelect=1
        displayUpdate()
        #rootCanvas.after(2000, rootCanvas.destroy)
        print("sleep2")
        time.sleep(2)
        colorSelect=2
        displayUpdate()
        #rootCanvas.after(2000, rootCanvas.destroy)
        print("sleep2")
        time.sleep(2)
        colorSelect=4
        displayUpdate()
        print("sleep2")
        time.sleep(2)
        colorSelect=7
        displayUpdate()
        
    
    def bit10(iself):
        global clutBits
        iself.CLUT10.config(bg='green4')
        iself.CLUT12.config(bg='gray80')
        clutBits=10
        #print (clutBits," 10")
        
    def bit12(iself):
        global clutBits
        iself.CLUT10.config(bg='gray80')
        iself.CLUT12.config(bg='green4')
        clutBits=12
        #print (clutBits, " 12")
# ************** Functions End ******************

rootButtons = MenuButtons(root)
displayUpdate()
gammaFigUpdate()
init_SLM_data()
root.mainloop()