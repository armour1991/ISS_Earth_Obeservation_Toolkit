import cv2
import numpy as np


def load_images(image1_path, image2_path):
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        raise FileNotFoundError("One or both images could not be loaded.")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    return img1, img2, gray1, gray2


def detect_features(gray1, gray2):
    orb = cv2.ORB_create(5000)

    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    return kp1, des1, kp2, des2


def match_features(img1, img2, kp1, kp2, des1, des2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    matches = matches[:200]

    matched_image = cv2.drawMatches(
        img1,
        kp1,
        img2,
        kp2,
        matches[:100],
        None,
        flags=2
    )

    return matches, matched_image


def display_matches(matched_image, scale=0.1):
    new_width = int(matched_image.shape[1] * scale)
    new_height = int(matched_image.shape[0] * scale)

    resized = cv2.resize(
        matched_image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    cv2.imshow("ORB Feature Matches", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def calculate_pixel_shift(kp1, kp2, matches):
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])

    M, mask = cv2.estimateAffinePartial2D(
        pts1,
        pts2,
        method=cv2.RANSAC
    )

    tx = M[0, 2]
    ty = M[1, 2]

    pixel_shift = np.sqrt(tx**2 + ty**2)
    
    return pixel_shift, M