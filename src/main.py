#!/usr/bin/python
import cv2
import threading
class cameras(threading.Thread):
	def __init__(self, camID, name, counter):
		threading.Thread.__init__(self)
		self.camID = camID
		self.name = name
		self.counter = counter
	def run(self):
		threading.Lock().acquire()
		show(self.camID)
		threading.Lock().release()
def listCam():
	index=0
	valid_cams = []
	while True:
		temp_cam = cv2.VideoCapture(index)
		if not temp_cam.isOpened():
			break
		else:
			ret,frame=temp_cam.read()
			if not ret:
				break
			else:
				valid_cams.append(index)
		index+=1
	return valid_cams
def show(index):
	cap = cv2.VideoCapture(index)
	while True:
		ret,frame = cap.read()
		cv2.imshow("camera "+str(index),frame)
		cv2.waitKey(10)
	cv2.destroyWindow("camera "+str(index))
def main():
	allCams = listCam()
	threads = []
	for i,num in enumerate(allCams):
		threads.append(cameras(num,"camera "+str(num),i))
		threads[i].start()
	for i in threads:
		i.join()
if __name__=="__main__":
	main()
