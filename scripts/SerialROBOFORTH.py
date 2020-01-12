
import serial,time,cv2,imutils,threading,r12
from DetectColoredBoxesFunc import DetectColoredBoxLocation
USBport='/dev/ttyUSB0'
#SerialReadTimeOut = 5 #wait 5 seconds

R17Robot = r12.Arm()
R17Robot.connect(USBport)
camera = cv2.VideoCapture(0)

POSDIC = {
'CAMERA' : 'DECIMAL 0 2349 3429 6609 2212 -6414 JMA',
'READY'  : 'DECIMAL 0 936 936 9999 10388 -6313 JMA',
'S1'     : 'DECIMAL 0 -719 -53 11893 12536 -7973 JMA',
'NEARS1' : 'DECIMAL 0 -622 41 12179 11402 -7973 JMA',
'S2'     : 'DECIMAL 0 -478 1182 7045 14820 -4421 JMA',
'NEARS2' : 'DECIMAL 0 -411 1249 7367 13780 -4420 JMA',
'S3'     : 'DECIMAL 0 -356 837 8629 13722 -6046 JMA',
'NEARS3' : 'DECIMAL 0 -248 942 9000 12350 -6045 JMA',
'S4'     : 'DECIMAL 0 249 1017 7822 14260 -7659 JMA',
'NEARS4' : 'DECIMAL 0 392 1112 8200 12934 -7659 JMA',
'S2UP2'     : 'DECIMAL 0 -421 1239 7349 13872 -4419 JMA',
'NEARS2UP2' : 'DECIMAL 0 -317 1343 7656 12632 -4417 JMA',
'S2UP1'     : 'DECIMAL 0 -435 1225 7163 14332 -4390 JMA',
'NEARS2UP1' : 'DECIMAL 0 -341 1319 7509 13070 -4390 JMA'}

COLINDEXDEC = {
'RED' 	: 0,
'BLUE'	: 1,
'YELLOW': 2}


BOXES_LOCATIONS = [None,None,None]
def DetectBoxesThread():
	global BOXES_LOCATIONS,camera
	while(True):
		(grabbed, frame) = camera.read()
		BOXES_LOCATIONS = DetectColoredBoxLocation(frame)   #Output Order: Red,BLue,Yellow \ Defined Locations: S1,S2,S3,S4
thrd = threading.Thread(target=DetectBoxesThread)	
thrd.daemon = True
thrd.start()

def COLDSTART():
	R17Robot.write('ROBOFORTH')
	print(R17Robot.read())

	R17Robot.write('START')
	print(R17Robot.read())

	R17Robot.write('CALIBRATE')
	print(R17Robot.read())

	R17Robot.write('HOME')
	print(R17Robot.read())

	R17Robot.write('JOINT')
	print(R17Robot.read())

	R17Robot.write(POSDIC['CAMERA'])
	print(R17Robot.read())

def GOTOCAMERA():
	R17Robot.write(POSDIC['CAMERA'])
	print(R17Robot.read())

def MOVEFT(SX,SY):
	R17Robot.write(POSDIC['READY'])
	print(R17Robot.read())
	R17Robot.write(POSDIC['NEAR'+SX])
	print(R17Robot.read())
	R17Robot.write(POSDIC[SX])
	print(R17Robot.read())
	R17Robot.write('GRIP')
	print(R17Robot.read())
	R17Robot.write(POSDIC['NEAR'+SX])
	print(R17Robot.read())
	R17Robot.write(POSDIC['READY'])
	print(R17Robot.read())
	R17Robot.write(POSDIC['NEAR'+SY])
	print(R17Robot.read())	
	R17Robot.write(POSDIC[SY])
	print(R17Robot.read())
	R17Robot.write('UNGRIP')
	print(R17Robot.read())
	R17Robot.write(POSDIC['NEAR'+SY])
	print(R17Robot.read())
	R17Robot.write(POSDIC['READY'])
	print(R17Robot.read())
	R17Robot.write(POSDIC['CAMERA'])
	print(R17Robot.read())

#while(True):
#	MSG = input("Enter Message: ")
#	R17Robot.write(MSG.upper())
#	print(R17Robot.read())

#while(True):
#	FROM = input("MOVE FROM: ")
#	if (FROM.upper() == 'START'):
#		COLDSTART()
#		continue
#	TO   = input("TO: ")
#	MOVEFT(FROM.upper(),TO.upper())


print("Choose BOX COLOR, then WHERE TO place it!\nDefined Locations: S1,S2,S3,S4\nHint: To calibrate, type FROM: 'START' ")
while(True):
	print('Detecting Boxes... Please wait...\nYou can type (START/CAMERA/ENTER)')
	while(BOXES_LOCATIONS == [None,None,None]):
		BOX_COLOR = input("(START/CAMERA/ENTER): ")
		if (BOX_COLOR.upper() == 'START'):
			COLDSTART()
		if (BOX_COLOR.upper() == 'CAMERA'):
			GOTOCAMERA()
		pass
	BOX_COLOR = input("BOX COLOR: ")
	if (BOX_COLOR.upper() == 'START'):
		COLDSTART()
		continue
	if (BOX_COLOR.upper() == 'CAMERA'):
		GOTOCAMERA()
		continue
	CURRENT_BOX_PLACE = BOXES_LOCATIONS[COLINDEXDEC[BOX_COLOR.upper()]]
	print (BOX_COLOR.upper(),' Box place:',CURRENT_BOX_PLACE)
	WHERE_TO = input('WHERE TO:')
	if (WHERE_TO.upper() == 'PASS'):
		continue
	MOVEFT(CURRENT_BOX_PLACE,WHERE_TO.upper())
	
	
R17Robot.disconnect()
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
