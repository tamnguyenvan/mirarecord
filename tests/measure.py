import cv2
from sys import argv


img = cv2.imread(argv[1])
h, w = img.shape[:2]
cv2.imshow('img', img[h//2:h, :, :])
cv2.waitKey()