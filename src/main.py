#!/usr/bin/python
import math
import numpy as np
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

	def get(self):
		return self.frame
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
def combine(cameraList):
	dx = int(1000/math.sqrt(len(cameraList)))
	dy = int(1000/(len(cameraList)/int(math.sqrt(len(cameraList)))))
	print(dy)
	img = [cv2.resize(cameraList[0].get(),(dx,dy),interpolation=cv2.INTER_AREA)]
	for i,camera in enumerate(cameraList):
		if(i==0):
			continue
		img[i%int(math.sqrt(len(cameraList)))] = np.concatenate((img[i%int(math.sqrt(len(cameraList)))],cv2.resize(camera.get(),(dx,dy),interpolation=cv2.INTER_AREA)),axis=0)
	finalImg=img[0]
	for i,image in enumerate(img):
		if(i==0):
			continue
		finalImg = np.concatenate((finalImg,image),axis=1)
	cv2.imshow("total",finalImg)
	cv2.waitKey(1)
def main():
	allCams = listCam()
	threads = []
	for i,num in enumerate(allCams):
		threads.append(cameras(num,"camera "+str(num),i))
		threads[i].start()
	while True:
		try:
			combine(threads)
		except AttributeError:
			pass
	for i in threads:
		i.join()
if __name__=="__main__":
	main()
