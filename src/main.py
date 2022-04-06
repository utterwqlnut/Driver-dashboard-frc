#!/usr/bin/python
import cv2
import threading
class cameras(threading.Thread):
	def __init__(self, camID, name, counter):
		threading.Thread.__init__(self)
		self.camID = camID
		self.name = name
		self.counter = counter
		self.cam = cv2.VideoCapture(camID)
	def run(self):
		while True:
			self.ret,self.frame = self.cam.read()

	def display(self):
		cv2.imshow("camera "+str(self.camID),self.frame)
		key = cv2.waitKey(0)
		if key== ord('q'):
			cv2.destroyAllWindows()
			exit(1)
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
def main():
	allCams = listCam()
	threads = []
	for i,num in enumerate(allCams):
		threads.append(cameras(num,"camera "+str(num),i))
		threads[i].start()
	while True:
		for j,i in enumerate(threads):
			try:
				i.display()
			except AttributeError:
				pass
		
	for i in threads:
		i.join()
if __name__=="__main__":
	main()
