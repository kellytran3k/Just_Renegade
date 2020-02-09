import numpy as np

HEAD = 0
NECK = 1
LEFT_SHOULDER = 2
LEFT_ELBOW = 3
LEFT_HAND = 4
RIGHT_SHOULDER = 5
RIGHT_ELBOW = 6
RIGHT_HAND = 7
LEFT_HIP = 8
LEFT_KNEE = 9
LEFT_HEEL = 10
LEFT_TOE = 11
RIGHT_HIP = 12
RIGHT_KNEE = 13
RIGHT_HEEL = 14
RIGHT_TOE = 15

def calcMag(a, b):
    return np.sqrt(
        (a[0] - b[0])**2 +
        (a[1] - b[1])**2
    )

def calcAngle(a, b, c):
    v1 = a - b
    v2 = c - b
    lv1 = np.linalg.norm(v1)
    lv2 = np.linalg.norm(v2)
    dp = np.dot(v1, v2)

    return np.arccos(dp / (lv1 * lv2))

def calcPoseComparand(p):
    #print(p)
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

def compare(a, b):
    diff = []
    for i, x in enumerate(a):
        if a[i] != 0 or b[i] != 0:
            diff.append(abs(a[i] - b[i]))
    
    return diff
