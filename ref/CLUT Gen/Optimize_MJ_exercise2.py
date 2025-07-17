# optimize MJ exercise
import scipy.optimize as spo 
import numpy as np
import matplotlib.pyplot as plt
#from scipy import optimize

gammaBits=8
clutBits=10
gammaN=2**gammaBits
clutN=2**clutBits
grayX = np.linspace(0, (gammaN-1), gammaN) # 0, 1, 2, ...255 should be (0, 1023, 1024)
slmXL=np.linspace(0, (clutN-1), clutN)
#slmX=int(slmXL)
#print (grayX)
x=grayX/255     # x[i] for gamma curve
x1=slmXL/1023    # x1[i] for SLM curve
gamma=x**2.2
#print (gamma)
#print (gamma[254])
# **************** ok to here ************
slmFunc=[]
slmX=[]
for i in range (0, clutN-1): # should be 1023 or 4095
    slmX.append(int(slmXL[i]))
    slmFunc.append(np.sin(1.2*x1[i]*np.pi/2-0.1)**2) # shifted and past-maxed sin^2 curve
    
#print ("sin: ", slmFunc) # [200])

minIndex=slmFunc.index(min(slmFunc))    # min/max search for truncation of SLM curve
maxIndex=slmFunc.index(max(slmFunc))
print("min/max ", minIndex, maxIndex)
print(slmFunc[minIndex], slmFunc[maxIndex]) # truncation verification

def f(slmX):
    k=slmX
    merit=(target-slmFunc[k])**2
    print ("slmF ", target, slmFunc[k])
    return merit

# starting guess
xyStart= minIndex # x start & y start

bnds = ((1,100))

# optimize
target= gamma[20]
result = spo.minimize(f, xyStart, options={"disp": True}) #, bounds=bnds) # options to display optimization info (iterations, function, gradient, etc.)
if result.success:
    xy=result.x  # x is whatever is optimizing
    print("Success", xy, slmFunc[int(xy)])
    print("target ", target)
else:
    print("Failed!")