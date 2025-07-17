#defining our append function
def appendList(l,element):
    for i in range(len(element)):
        l[i].append(element[i])
    return l

#defining a 2D list
#myList = [[],[],[]]
myList = [[],[],[]]
print ("start ", myList)
#new element
newList = [4,5,6]
newList1 = [7,8,9]
newList2 = [10,11,12]

#function calling
myList = appendList(myList,newList)
myList = appendList(myList,newList1)
myList = appendList(myList,newList2)
print(myList)

mList =[[]]*3   # initial appearace is same, but not same as declaration: myList = [[],[],[]]
print(mList)        # 
for i in range(0,3):
    myList[1][i]=0
print(myList)

mList=appendList(mList, newList)
mList=appendList(mList, newList1)
#mList=appendList(mList, [4,5,6])
print(mList)

nList = [[]*1 for i in range(3)] #  !!!!! Fix for above issue !!!!!
print (nList)
nList=appendList(nList, newList)
nList=appendList(nList, newList1)
print (nList)

tempList =[]
tempList.append(0)
tempList.append(1)
tempList.append(2)
print (tempList)
nList=appendList(nList, tempList)
print (nList)
print (nList[2][1]) # [gray][color]

temp=nList[1][1]
print (temp)
