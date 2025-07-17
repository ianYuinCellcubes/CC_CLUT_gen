import numpy as np
import matplotlib.pyplot as plt

gammaBits=8
clutBits=10
gammaN=2**gammaBits
clutN=2**clutBits
grayX = np.linspace(0, (gammaN-1), gammaN) # 0, 1, 2, ...255 should be (0, 1023, 1024)
slmX=np.linspace(0, (clutN-1), clutN)
#print (grayX)
x=grayX/255     # x[i] for gamma curve
x1=slmX/1023    # x1[i] for SLM curve
y=x**2.2
# **************** ok to here ************
slmFunc=[]
for i in range (0, clutN-1): # should be 1023 or 4095
    slmFunc.append(np.sin(1.2*x1[i]*np.pi/2-0.1)**2) # shifted and past-maxed sin^2 curve
    
print ("sin: ", slmFunc) # [200])

minIndex=slmFunc.index(min(slmFunc))    # min/max search for truncation of SLM curve
maxIndex=slmFunc.index(max(slmFunc))
print("min/max ", minIndex, maxIndex)
print(slmFunc[minIndex], slmFunc[maxIndex]) # truncation verification
slmTruncated=slmFunc[minIndex: (maxIndex+1)] # truncated response

def appendList(l,element):
    for i in range(len(element)):
        l[i].append(element[i])
    return l

clut=[[]*1 for i in range(gammaN)]

for color in range(0,3):
    tempList=[] # To simulate 3 columnrow/column data
    for k in range (0, gammaN):
        searchVal=y[k]
        difference_array = np.absolute(slmTruncated-searchVal) # form absolute difference array to find min difference
        index = difference_array.argmin()                       # min difference == searched index
        nIndex= index.item() + minIndex - color            # -color is just to add variation to data set
        tempList.append(nIndex) # clut index array
    #   print(tempList)
    clut=appendList(clut, tempList)
print(clut)

#aa=slmTruncated[index]
#print("Nearest element to the given values is : ", slmTruncated[index], slmFunc[index+minIndex])
#print("Index of nearest value is : ", index, index+minIndex)