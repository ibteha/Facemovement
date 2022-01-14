# import cv2
# from PIL import Image
# import numpy as np

# face_detector = cv2.CascadeClassifier("/content/drive/My Drive/Ayush Gupta/Image-animation/first-order-motion/first-order-model/alignment/haarcascade_frontalface_default.xml")
# eye_detector = cv2.CascadeClassifier("/content/drive/My Drive/Ayush Gupta/Image-animation/first-order-motion/first-order-model/alignment/haarcascade_eye.xml")
# img = cv2.imread("/content/drive/My Drive/Ayush Gupta/Image-animation/first-order-motion/first-order-model/alignment/image.png")
# print(len(img))
# img_raw = img.copy()
# faces = face_detector.detectMultiScale(img)

# #if len(x)==0:
#  #   pass
# #else:
# face_x, face_y, face_w, face_h = faces[0]

 
# img = img[int(face_y):int(face_y+face_h), int(face_x):int(face_x+face_w)]
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# eyes = eye_detector.detectMultiScale(img_gray)
 
# index = 0
# for (eye_x, eye_y, eye_w, eye_h) in eyes:
#    if index == 0:
#       eye_1 = (eye_x, eye_y, eye_w, eye_h)
#    elif index == 1:
#       eye_2 = (eye_x, eye_y, eye_w, eye_h)
 
#    cv2.rectangle(img,(eye_x, eye_y),(eye_x+eye_w, eye_y+eye_h), color, 2)
#    index = index + 1
#    if eye_1[0] < eye_2[0]:
#    	left_eye = eye_1
#    	right_eye = eye_2
#    else:
#    	left_eye = eye_2
#    	right_eye = eye_1	

#    left_eye_center = (int(left_eye[0] + (left_eye[2] / 2)), int(left_eye[1] + (left_eye[3] / 2)))
#    left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
 
#    right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
#    right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]
 
#    cv2.circle(img, left_eye_center, 2, (255, 0, 0) , 2)
#    cv2.circle(img, right_eye_center, 2, (255, 0, 0) , 2)
#    cv2.line(img,right_eye_center, left_eye_center,(67,67,67),2)
#    if left_eye_y < right_eye_y:
#     point_3rd = (right_eye_x, left_eye_y)
#     direction = -1 #rotate same direction to clock
#     print("rotate to clock direction")
#    else:
#     point_3rd = (left_eye_x, right_eye_y)
#     direction = 1 #rotate inverse direction of clock
#     print("rotate to inverse clock direction")
 
#    cv2.circle(img, point_3rd, 2, (255, 0, 0) , 2)
 
#    cv2.line(img,right_eye_center, left_eye_center,(67,67,67),2)
#    cv2.line(img,left_eye_center, point_3rd,(67,67,67),2)
#    cv2.line(img,right_eye_center, point_3rd,(67,67,67),2)
# def euclidean_distance(a, b):
# 	x1 = a[0]; y1 = a[1]
# 	x2 = b[0]; y2 = b[1]
# 	return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
# 	a = euclidean_distance(left_eye_center, point_3rd)
# 	b = euclidean_distance(right_eye_center, left_eye_center)
# 	c = euclidean_distance(right_eye_center, point_3rd)
# 	cos_a = (b*b + c*c - a*a)/(2*b*c)
# 	print("cos(a) = ", cos_a)
	 
# 	angle = np.arccos(cos_a)
# 	print("angle: ", angle," in radian")
	 
# 	angle = (angle * 180) / math.pi
# 	print("angle: ", angle," in degree")
  
#   if direction == -1:
# 	   angle = 90 - angle
#   new_img = Image.fromarray(img_raw)
#   new_img = np.array(new_img.rotate(direction * angle))



import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from PIL import Image

#------------------------

def euclidean_distance(a, b):
	x1 = a[0]; y1 = a[1]
	x2 = b[0]; y2 = b[1]
	
	return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))

def detectFace(img):
	faces = face_detector.detectMultiScale(img, 1.3, 5)
	#print("found faces: ", len(faces))

	if len(faces) > 0:
		face = faces[0]
		face_x, face_y, face_w, face_h = face
		img = img[int(face_y):int(face_y+face_h), int(face_x):int(face_x+face_w)]
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		return img, img_gray
	else:
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return img, img_gray
		#raise ValueError("No face found in the passed image ")

def alignFace(img_path):
	img = cv2.imread(img_path)
	plt.imshow(img[:, :, ::-1])
	plt.show()

	img_raw = img.copy()

	img, gray_img = detectFace(img)
	
	eyes = eye_detector.detectMultiScale(gray_img)
	
	#print("found eyes: ",len(eyes))
	
	if len(eyes) >= 2:
		#find the largest 2 eye
		
		base_eyes = eyes[:, 2]
		#print(base_eyes)
		
		items = []
		for i in range(0, len(base_eyes)):
			item = (base_eyes[i], i)
			items.append(item)
		
		df = pd.DataFrame(items, columns = ["length", "idx"]).sort_values(by=['length'], ascending=False)
		
		eyes = eyes[df.idx.values[0:2]]
		
		#--------------------
		#decide left and right eye
		
		eye_1 = eyes[0]; eye_2 = eyes[1]
		
		if eye_1[0] < eye_2[0]:
			left_eye = eye_1
			right_eye = eye_2
		else:
			left_eye = eye_2
			right_eye = eye_1
		
		#--------------------
		#center of eyes
		
		left_eye_center = (int(left_eye[0] + (left_eye[2] / 2)), int(left_eye[1] + (left_eye[3] / 2)))
		left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
		
		right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
		right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]
		
		#center_of_eyes = (int((left_eye_x+right_eye_x)/2), int((left_eye_y+right_eye_y)/2))
		
		cv2.circle(img, left_eye_center, 2, (255, 0, 0) , 2)
		cv2.circle(img, right_eye_center, 2, (255, 0, 0) , 2)
		#cv2.circle(img, center_of_eyes, 2, (255, 0, 0) , 2)
		
		#----------------------
		#find rotation direction
		
		if left_eye_y > right_eye_y:
			point_3rd = (right_eye_x, left_eye_y)
			direction = -1 #rotate same direction to clock
			print("rotate to clock direction")
		else:
			point_3rd = (left_eye_x, right_eye_y)
			direction = 1 #rotate inverse direction of clock
			print("rotate to inverse clock direction")
		
		#----------------------
		
		cv2.circle(img, point_3rd, 2, (255, 0, 0) , 2)
		
		cv2.line(img,right_eye_center, left_eye_center,(67,67,67),1)
		cv2.line(img,left_eye_center, point_3rd,(67,67,67),1)
		cv2.line(img,right_eye_center, point_3rd,(67,67,67),1)
		
		a = euclidean_distance(left_eye_center, point_3rd)
		b = euclidean_distance(right_eye_center, point_3rd)
		c = euclidean_distance(right_eye_center, left_eye_center)
		
		#print("left eye: ", left_eye_center)
		#print("right eye: ", right_eye_center)
		#print("additional point: ", point_3rd)
		#print("triangle lengths: ",a, b, c)
		
		cos_a = (b*b + c*c - a*a)/(2*b*c)
		#print("cos(a) = ", cos_a)
		angle = np.arccos(cos_a)
		#print("angle: ", angle," in radian")
		
		angle = (angle * 180) / math.pi
		print("angle: ", angle," in degree")
		
		if direction == -1:
			angle = 90 - angle
		
		print("angle: ", angle," in degree")
		
		#--------------------
		#rotate image
		
		new_img = Image.fromarray(img_raw)
		new_img = np.array(new_img.rotate(direction * angle))
	
	return new_img
	
#------------------------

#opencv path

opencv_home = cv2.__file__
folders = opencv_home.split(os.path.sep)[0:-1]

path = folders[0]
for folder in folders[1:]:
	path = path + "/" + folder

face_detector_path = "/content/drive/My Drive/Ibtehaj/FSGAN/First_order_motion/implemented/first-order-motion/first-order-model/alignment/haarcascade_frontalface_default.xml"
eye_detector_path = "/content/drive/My Drive/Ibtehaj/FSGAN/First_order_motion/implemented/first-order-motion/first-order-model/alignment/haarcascade_eye.xml"
nose_detector_path = path+"/data/haarcascade_mcs_nose.xml"

if os.path.isfile(face_detector_path) != True:
	raise ValueError("Confirm that opencv is installed on your environment! Expected path ",detector_path," violated.")

face_detector = cv2.CascadeClassifier(face_detector_path)
eye_detector = cv2.CascadeClassifier(eye_detector_path) 
nose_detector = cv2.CascadeClassifier(nose_detector_path) 

#------------------------

#test_set = ["angelina.jpg", "angelina2.jpg", "angelina3.jpg"]
image1= ["/content/drive/MyDrive/Ibtehaj/FSGAN/First_order_motion/implemented/first-order-motion/first-order-model/input/2.png"]

alignedFace = alignFace(image1)
plt.imshow(alignedFace[:, :, ::-1])
plt.show()
img, gray_img = detectFace(alignedFace)
plt.imshow(img[:, :, ::-1])
plt.show()