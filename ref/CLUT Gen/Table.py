# Python program to create a table

from tkinter import *

def TT(root):    # code for creating table
    for i in range(1, total_rows+1):
        for j in range(0, total_columns):
            example = Entry(root, width=10, fg='blue', font=('Arial',12,'bold'))
            example.grid(row=i, column=j)
            example.insert(END, lst[i-1][j])
            
class Table:
	
	def __init__(self,root):    # code for creating table
		for i in range(total_rows): 

			for j in range(total_columns):
				
				self.example = Entry(root, width=10, fg='blue', font=('Arial',12,'bold'))
				self.example.grid(row=i, column=j)
				self.example.insert(END, lst[i][j])

# take the data
lst = [(1,'Raj','Mumbai',19),
	(2,'Aaryan','Pune',18),
	(3,'Vaishnavi','Mumbai',20),
	(4,'Rachna','Mumbai',21),
	(5,'Shubham','Delhi',21)]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])

# create root window
root = Tk()

for k in range(3):
    ex = Entry(root, width=10, fg='blue', font=('Arial',12,'bold'))
    ex.grid(row=0, column=k)
    ex.insert(END, "Gray")
#t = Table(root)
tt= TT(root)
root.mainloop()
