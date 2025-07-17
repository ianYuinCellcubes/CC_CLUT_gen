'''     
        Brent Method good for analog optimization f(x), x is float variable that is not definable
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

gammaBits=8
clutBits=10
gammaN=2**gammaBits
clutN=2**clutBits
grayX = np.linspace(0, (gammaN-1), gammaN) # 0, 1, 2, ...255 should be (0, 1023, 1024)
slmX=np.linspace(0, (clutN-1), clutN)
#print (grayX)
x=grayX/255     # x[i] for gamma curve
x1=slmX/1023    # x1[i] for SLM curve
gamma=x**2.2
#print (gamma)
#print (gamma[254])
# **************** ok to here ************
slmFunc=[]
for i in range (0, clutN-1): # should be 1023 or 4095
    slmFunc.append(np.sin(1.2*x1[i]*np.pi/2-0.1)**2) # shifted and past-maxed sin^2 curve
    
print ("sin: ", slmFunc) # [200])

minIndex=slmFunc.index(min(slmFunc))    # min/max search for truncation of SLM curve
maxIndex=slmFunc.index(max(slmFunc))
print("min/max ", minIndex, maxIndex)
print(slmFunc[minIndex], slmFunc[maxIndex]) # truncation verification

def searchIndex(target, clutIndex):
    x=1
    
def f(targetVal, slmX):
    meritF=(targetVal-slmFunc[slmX])**2
    return meritF   # also tracks slmX as result.slmX ??

clut=[]
k=0
