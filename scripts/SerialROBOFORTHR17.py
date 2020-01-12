

import serial,time
import st

USBport='/dev/ttyUSB0'
BaudRate = 19200
#SerialReadTimeOut = 5 #wait 5 seconds

R17Robot = st.StArm(USBport,BaudRate)


