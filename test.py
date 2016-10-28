import cv2

print"hello workd"
img = cv2.imread('images/0.3_100.JPG',0)
cv2.imshow('window_name',img)
cv2.waitKey(5000)
cv2.destroyAllWindows()
