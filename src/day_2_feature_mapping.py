import cv2 

img1 = cv2.imread("C:/Amritbir_1024150159/ISS Earth Observation Toolkit/Data/raw_images/image1.jpg")
img2 = cv2.imread("C:/Amritbir_1024150159/ISS Earth Observation Toolkit\Data/raw_images/image2.jpg")

print(img1.shape)
print(img2.shape)

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(5000)

kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

print(len(kp1))
print(len(kp2))

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1,des2)
matches = sorted(matches, key=lambda x: x.distance)
print(len(matches))

matched = cv2.drawMatches(
    img1,
    kp1,
    img2,
    kp2,
    matches[:100],
    None,
    flags=2
)

scale = 0.1
new_width = int(matched.shape[1]*scale)
new_height = int(matched.shape[1]*scale)

matched_resized = cv2.resize(
    matched,
    (new_width, new_height),
    interpolation=cv2.INTER_AREA
)

cv2.imshow("ORB Feature Matches", matched_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
pts2 = np.float32([kp2[m.queryIdx].pt for m in matches])

M, mask = cv2.estimateAffinePartial2D(
    pts1,
    pts2,
    method=cv2.RANSAC
)
print(M)

tx = M[0,2]
ty = M[1,2]

print(f"tx = {M[0,2]:.2f}")
print(f"ty = {M[1,2]:.2f}")
pixel_shift = np.sqrt(tx**2 + ty**2)
print(pixel_shift)