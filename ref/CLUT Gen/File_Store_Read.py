
import numpy as np

x = np.linspace(0,100,201)
y = np.random.random(201)

with open('BD_data.dat', 'w') as f:
    for i in range(len(x)):
        f.write('{:4.1f} {:.4f}\n'.format(x[i], y[i])) # Check the saved file, you will see
                        #the two columns of data, separated by a space.
                        # #You can change the write line in different ways, for example, you could have:
                        # f.write('{:4.1f}\t{:.4f}\n'.format(x[i], y[i]))
                        # which will add a tab between the columns, and not a space.
                        # https://pythonforthelab.com/blog/introduction-to-storing-data-in-files/


f = open("demofile3.txt", "w")  # "replace with "a" for append
f.write("Woops! I have deleted the content!")
f.close()

#open and read the file after the overwriting:
f = open("demofile3.txt", "r")
print(f.read())