#
# Serial interface to Arduino
#

import serial.tools.list_ports  # pip install pyserial to interface to Arduino

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:   # string version of ports list
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

for i in range(len(portsList)):
    if portsList[i].startswitch("COM"+str(com)):
        use = "COM"+ str(com)
        print(use)
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

while True:
    command = input("Arduino Command (ON/OFF/exit)")
    serialInst.write(command.encode('utf-8'))
    
    if command =='exit':
        exit()
        
        