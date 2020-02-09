import json
import analyse_pose as ap
import numpy as np
import math

#the command in linux syntax: 
# `./bin/OpenPoseDemo.exe --net_resolution "128x128" --video ../../renegadeVid.avi 
# --write_json output/ --display 0 --render_pose 0 --keypoint_scale 3`

angle_diffs = []
index = 100
while index < 400:
    with open('trish_output/media.io_trishRenegadeVid_000000000'+str(index)+'_keypoints.json') as f:
        data = json.load(f)

    keypoints = data["people"][0]["pose_keypoints_2d"]
    l = [x for i, x in enumerate(keypoints) if (i+1) % 3 != 0]
    xy = [l[(i*2):((i*2)+2)] for i in range((len(l)+1) // 2)]
    point_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 23, 12, 13, 14, 20]
    points = [np.asarray(xy[i]) for i in point_indexes]
    #print(points)

    with open('tempoutput/mirror1_000000000'+str(index)+'_keypoints.json') as f1:
        data1 = json.load(f1)

    keypoints1 = data1["people"][0]["pose_keypoints_2d"]
    l1 = [x for i, x in enumerate(keypoints1) if (i+1) % 3 != 0]
    xy1 = [l1[(i*2):((i*2)+2)] for i in range((len(l1)+1) // 2)]
    point_indexes1 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 23, 12, 13, 14, 20]
    points1 = [np.asarray(xy1[i]) for i in point_indexes]
    #print(points1)

    # reflect = [5, 6, 7, 12, 13, 14, 15]
    # for i in reflect:
    #     points[i][0] = 1 - points[i][0]
    #     points1[i][0] = 1 - points1[i][0]

    radians = ap.calcPoseComparand(points)
    degrees = []
    for x in radians:
        degrees.append(x * (180/math.pi))
    #print(degrees)

    radians1 = ap.calcPoseComparand(points1)
    degrees1 = []
    for x in radians1:
        degrees1.append(x * (180/math.pi))
    #print(degrees1)

    diff = ap.compare(degrees, degrees1)
    angle_diffs.append(diff[0])
    angle_diffs.append(diff[2])

    index += 10

sum = 0
for x in angle_diffs:
    sum += x

print("You were on average " + str(sum / len(angle_diffs)) + " degrees off from Trish from TikTok.")