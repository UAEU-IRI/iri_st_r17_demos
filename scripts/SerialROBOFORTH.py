

import serial,time

#ser = serial.Serial('/dev/ttyUSB0', 19200)

ser = serial.Serial(
  port='/dev/ttyUSB0',
  baudrate = 19200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

print ("Serial is open: " + str(ser.isOpen()))

#ser.write('ROBOFORTH\r')
ser.write('CALIBRATE\r')

while True:
	x = ser.read()
	print ('x is:',x)
        #line.append(c)
	
        #if c == '\r':
        #    print("Line: " + ''.join(line))
        #    line = []
        #    break



#while(x != "OK"):
#	x = ser.readline()
#print ("Recieved:",x)

#time.sleep(1)
#ser.write('JOINT\r')
#time.sleep(1)
#ser.write('START\r')
#time.sleep(1)
#ser.write('CALIBRATE\r')
#time.sleep(1)
#ser.write('HOME\r')
#time.sleep(2)

#print ("Did write, now read")
#x = ser.readline()
#print ("got '" + x + "'")
ser.close()
