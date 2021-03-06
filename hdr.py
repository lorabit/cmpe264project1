import cv2
import os
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
import numpy as np
from math import log

sample_rect = (1300,1300,100,100)
channel = 2

exposure_times = []
sample_values = []
count = 0
g_channels = [1.484, 1.962, 2.308]

# def sample(filename):
# 	image = cv2.imread('hdr/'+filename)
# 	ret = 0
# 	sample_image = np.zeros((sample_rect[2],sample_rect[3],3), np.uint8)
# 	for i in range(0,sample_rect[2]):
# 		for j in range(0,sample_rect[3]):
# 			sample_image[i][j] = [image[i+sample_rect[0]][j+sample_rect[1]][channel]]*3
# 			ret = ret + image[i+sample_rect[0]][j+sample_rect[1]][channel]
# 	cv2.imwrite('t/samples/'+str(count)+'_'+str(channel)+'.jpg',sample_image)
# 	return float(ret)/(sample_rect[2]*sample_rect[3])

def exposure(filename):
	image = Image.open('hdr/'+filename)
	info = image._getexif()
	exposure_time = info[33434]
	print(exposure_time)
	return float(exposure_time[0])/exposure_time[1]

def linealized(filename,a):
	image = cv2.imread('hdr/'+filename)
	if a == 1:
		return image
	new_image = np.zeros(image.shape, np.float)
	multipler = [pow(a,1.0/g_channels[k]) for k in range(3)]
	for i in range(image.shape[0]):
		line = image[i]
		for j in range(image.shape[1]):
			row = line[j]
			for k in range(3):
				new_image[i][j][k] = row[k]*multipler[k]
	cv2.imwrite('hdr/linealized/'+filename,new_image)
	return new_image

def simple_linear(filename):
	image = cv2.imread('hdr/'+filename)
	new_image = np.zeros(image.shape, np.float)
	for i in range(image.shape[0]):
		line = image[i]
		for j in range(image.shape[1]):
			row = line[j]
			for k in range(3):
				new_image[i][j][k] = pow(row[k],g_channels[k])/pow(255,g_channels[k]-1)
	cv2.imwrite('hdr/simple_linear/'+filename,new_image)
	return new_image

files = os.listdir('hdr')
valid_files = []
for filename in files:
	if filename[-3:].lower()=='jpg':
		exposure_times.append(exposure(filename))
		valid_files.append(filename)


#Simple Linearization 
#After Linearization then creat combined HDR image by ziqiang
imgs = []
for filename in valid_files:
	imgs.append(simple_linear(filename))

HDR_img_method_1 = np.zeros(imgs[0].shape, np.float32)
HDR_img_method_2 = np.zeros(imgs[0].shape, np.float32)
HDR_img_method_3 = np.zeros(imgs[0].shape, np.float32)

threshold = 200

for i in  range(len(imgs[0])):
	for j in range(len(imgs[0][0])):
		for k in range(len(imgs[0][0][0])):
			if imgs[2][i][j][k] < threshold:
				HDR_img_method_1[i][j][k] = imgs[2][i][j][k] * (exposure_times[0]/exposure_times[2])
			elif imgs[1][i][j][k] <threshold:
				HDR_img_method_1[i][j][k] = imgs[1][i][j][k] * (exposure_times[0]/exposure_times[1])
			else:
				HDR_img_method_1[i][j][k] = imgs[0][i][j][k]

cv2.imwrite('hdr/combined/HDR_img_method_1.jpg',HDR_img_method_1)


for i in  range(len(imgs[0])):
	for j in range(len(imgs[0][0])):
		for k in range(len(imgs[0][0][0])):
			s = imgs[0][i][j][k] 
			n = 1
			if imgs[2][i][j][k] < threshold:
				n = n +1
				s = s + imgs[2][i][j][k] * (exposure_times[0]/exposure_times[2])
			if imgs[1][i][j][k] <threshold:
				n = n + 1
				s = s + imgs[1][i][j][k] * (exposure_times[0]/exposure_times[1])
			HDR_img_method_2[i][j][k] = s/n

cv2.imwrite('hdr/combined/HDR_img_method_2.jpg',HDR_img_method_2)

a1 = exposure_times[1]/exposure_times[0]
a2 = exposure_times[2]/exposure_times[0]

weight1 = 1/(pow(a1,2))
weight2 = 1/(pow(a2,2))

for i in  range(len(imgs[0])):
	for j in range(len(imgs[0][0])):
		for k in range(len(imgs[0][0][0])):
			s = imgs[0][i][j][k] 
			n = 1
			if imgs[2][i][j][k] < threshold:
				n = n + weight2
				s = s + weight2 * imgs[2][i][j][k] * (exposure_times[0]/exposure_times[2])
			if imgs[1][i][j][k] <threshold:
				n = n + weight1
				s = s + weight1 * imgs[1][i][j][k] * (exposure_times[0]/exposure_times[1])
			HDR_img_method_3[i][j][k] = s/n

cv2.imwrite('hdr/combined/HDR_img_method_3.jpg',HDR_img_method_3)

# tone map ziqiang
gam_value = 2.2
tonemap1 = cv2.createTonemapDurand(gamma=gam_value)
res_tonemap1 = tonemap1.process(HDR_img_method_1.copy())
res_tonemap1_8bit = np.clip(res_tonemap1*255, 0, 255).astype('uint8')
cv2.imwrite("hdr/tonemapped/res_tonemap1_8bit.jpg", res_tonemap1_8bit)


tonemap2 = cv2.createTonemapDurand(gamma=gam_value)
res_tonemap2 = tonemap2.process(HDR_img_method_2.copy())
res_tonemap2_8bit = np.clip(res_tonemap2*255, 0, 255).astype('uint8')
cv2.imwrite("hdr/tonemapped/res_tonemap2_8bit.jpg", res_tonemap2_8bit)


tonemap3 = cv2.createTonemapDurand(gamma=gam_value)
res_tonemap3 = tonemap3.process(HDR_img_method_3.copy())
res_tonemap3_8bit = np.clip(res_tonemap3*255, 0, 255).astype('uint8')
cv2.imwrite("hdr/tonemapped/res_tonemap3_8bit.jpg", res_tonemap3_8bit)


# Average HDR
# dest_exposure_time = 1.0/10.0
# print('linealizing image 0...')
# img1 = linealized(valid_files[0],dest_exposure_time/exposure_times[0])
# print('linealizing image 1...')
# img2 = linealized(valid_files[1],dest_exposure_time/exposure_times[1])
# print('linealizing image 2...')
# img3 = linealized(valid_files[2],dest_exposure_time/exposure_times[2])
# print('generating HDR image...')

# new_image = np.zeros(img1.shape, np.float)
# for i in range(img1.shape[0]):
# 	for j in range(img1.shape[1]):
# 		for k in range(3):
# 			new_image[i][j][k] = (img1[i][j][k] + img2[i][j][k] + img3[i][j][k])/3
# cv2.imwrite('hdr/linealized/avg.jpg',new_image) 

