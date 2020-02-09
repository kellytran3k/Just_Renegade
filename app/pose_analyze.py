import numpy as np

HEAD = 0
NECK = 1
LEFT_SHOULDER = 2
LEFT_ELBOW = 3
LEFT_HAND = 4
RIGHT_SHOULDER = 5
RIGHT_ELBOW = 6
RIGHT_HAND = 7
LEFT_HIP = 9
LEFT_KNEE = 10
LEFT_HEEL = 11
LEFT_TOE = 23
RIGHT_HIP = 12
RIGHT_KNEE = 13
RIGHT_HEEL = 14
RIGHT_TOE = 20

def calcMag(a, b):
    return np.sqrt(
        (a[0] - b[0])**2 +
        (a[1] - b[1])**2
    )

def calcAngle(a, b, c):
    ab = calcMag(a, b)
    ac = calcMag(a, c)
    bc = calcMag(b, c)

    numer = ab**2 + ac**2 + bc**2
    denom = 2 * ab * ac

    return np.arccos(numer / denom)

def calcPoseComparand(p):
    return np.asarray([
        # Left shoulder angle
        calcAngle(p[HEAD], p[NECK], p[LEFT_SHOULDER]),
        # Left elbow angle
        calcAngle(p[LEFT_SHOULDER], p[LEFT_ELBOW], p[LEFT_HAND]),
        # Right shoulder angle
        calcAngle(p[HEAD], p[NECK], p[RIGHT_SHOULDER]),
        # Right elbow angle
        calcAngle(p[RIGHT_SHOULDER], p[RIGHT_ELBOW], p[RIGHT_HAND]),
        # Left knee angle
        calcAngle(p[LEFT_HIP], p[LEFT_KNEE], p[LEFT_HEEL]),
        # Left foot angle
        calcAngle(p[LEFT_KNEE], p[LEFT_HEEL], p[LEFT_TOE]),
        # Right knee angle
        calcAngle(p[RIGHT_HIP], p[RIGHT_KNEE], p[RIGHT_HEEL]),
        # Right foot angle
        calcAngle(p[RIGHT_KNEE], p[RIGHT_HEEL], p[RIGHT_TOE])
    ])