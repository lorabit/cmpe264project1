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

def sample(filename):
	image = cv2.imread('t/'+filename)
	ret = 0
	sample_image = np.zeros((sample_rect[2],sample_rect[3],3), np.uint8)
	for i in range(0,sample_rect[2]):
		for j in range(0,sample_rect[3]):
			sample_image[i][j] = [image[i+sample_rect[0]][j+sample_rect[1]][channel]]*3
			ret = ret + image[i+sample_rect[0]][j+sample_rect[1]][channel]
	cv2.imwrite('t/samples/'+str(count)+'_'+str(channel)+'.jpg',sample_image)
	return float(ret)/(sample_rect[2]*sample_rect[3])

def exposure(filename):
	image = Image.open('t/'+filename)
	info = image._getexif()
	exposure_time = info[33434]
	print(exposure_time)
	return float(exposure_time[0])/exposure_time[1]

files = os.listdir('t')
for filename in files:
	if filename[-3:].lower()=='jpg':
		exposure_times.append(log(exposure(filename)))
		sample_values.append(log(sample(filename)))
		count = count + 1

print(exposure_times)
print(sample_values)

regr = linear_model.LinearRegression()

# Train the model using the training sets
train_x = np.array(exposure_times).reshape(len(exposure_times),1)
train_y = np.array(sample_values).reshape(len(sample_values),1)
regr.fit(train_x, train_y)

# The coefficients
print(regr.coef_)
g = regr.coef_[0][0]
print(1/g)
print(regr.intercept_)
print(np.mean((regr.predict(train_x) - train_y) ** 2))

fited_x = train_x
fited_y = regr.predict(fited_x)

plt.scatter(exposure_times,sample_values,color ='Red')
plt.plot(fited_x,fited_y)
plt.plot()
plt.xlabel('T(s)')
plt.ylabel('B\'^g')
plt.show()
		# for tag, value in info.items():
		# 	decoded = TAGS.get(tag, tag)
		# 	print(decoded)
		# 	print(tag)
