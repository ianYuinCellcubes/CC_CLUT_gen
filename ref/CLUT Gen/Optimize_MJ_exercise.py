# optimize MJ exercise
import scipy.optimize as spo 
import numpy as np
import matplotlib.pyplot as plt
#from scipy import optimize  https://www.geeksforgeeks.org/python-program-to-find-closest-number-in-array/

gammaBits=8
clutBits=10
gammaN=2**gammaBits
clutN=2**clutBits
grayX=[]
x=[]
gamma=[]
for i in range (0, 255):
    grayX.append(i)
    x.append(float(grayX[i]/255))
    gamma.append(float(x[i]**2.2))
    
#grayX = np.linspace(0, (gammaN-1), gammaN) # 0, 1, 2, ...255 should be (0, 1023, 1024)
slmX=np.linspace(0, (clutN-1), clutN)
#print (grayX)
#x=grayX/255     # x[i] for gamma curve
x1=slmX/1023    # x1[i] for SLM curve
#gamma=x**2.2
#print (gamma)
#print (gamma[254])
# **************** ok to here ************
slmFunc=[]
for i in range (0, clutN-1): # should be 1023 or 4095
    slmFunc.append(np.sin(1.2*x1[i]*np.pi/2-0.1)**2) # shifted and past-maxed sin^2 curve

minIndex=slmFunc.index(min(slmFunc))    # min/max search for truncation of SLM curve
maxIndex=slmFunc.index(max(slmFunc))
print("min/max ", minIndex, maxIndex)
print(slmFunc[minIndex], slmFunc[maxIndex]) # truncation verification

def f(x):
    
    area = (70-x)**2
    print ("a", area, x)
    return area

# starting guess
xyStart= 0# x start & y start


# optimize
result = spo.minimize(f, xyStart, options={"disp": True}) # bounds=bnds) # options to display optimization info (iterations, function, gradient, etc.)
if result.success:
    xy=result.x  # x is whatever is optimizing
    print("Success OK", xy)
    element=str(xy)
    print (grayX, grayX.index(int(xy+0.1)))
else:
    print("Failed!")