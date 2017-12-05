import dlib
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import os
import sys
from multiprocessing import Process
import time
from .eyeLike.eyeLike import *
import re
import json

#from eyeLike.eyeLike import *


dirname, filename = os.path.split(os.path.abspath(__file__))

predictor_name = "shape_predictor_68_face_landmarks.dat"
predictor_path = os.path.join(dirname, predictor_name)

#print ("real path is " + dirname)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

THREADS_NUM = 4
CURRENT_THREAD_NUM = -1
STEP_SIZE = 1

# got this data by testing. It is length of jawline to length of line connecting 14 and 7.
PROPORTION = 1.02

# x from left to right
# y from top to bottom
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ImageProcessor():
    POINT_SIZE = 3
    POINT_COLOR = (255, 0, 0)
    BASE_NAME = "pic"
    def __init__(self, path_to_pics, base_name, extension, index=None):
        self.path_to_pics = path_to_pics
        self.base_name = base_name
        self.ext = extension
        self.data = {}
        self.index = index
        if(self.index):
            self.index = str(index)
        else:
            self.index = ''

    def process_images(self, beginIndex, endIndex):
        # this doesn't include endIndex
        frames_data = {}
        counter = beginIndex
        for num in range(beginIndex, endIndex):
            points_data = {}
            pic_name = self.base_name + str(num) + '.' + self.ext
            print(pic_name)
            pic_path = os.path.join(self.path_to_pics, pic_name)
            # this is for last thread to avoid doing math.
            if(not os.path.exists(pic_path)):
                continue
            self.draw_points(pic_path, points_data)
            frames_data[counter] = points_data
            counter = counter + 1
        self.drop_data('data', self.data)
        self.drop_data('points', frames_data)

    def draw_points(self, pic_path, points_data):
        """
        Takes a picture, detects a face and draws all the points.
        args: a full path to the picture
        """
        # Pupil Finding here
        #pupils = get_eye_locations_in_image(pic_path)
        img = cv2.imread(pic_path)
        print (pic_path)
        print(os.path.exists(pic_path))
        frame_number = int(re.findall(r'\d+', pic_path.split('/')[-1])[0])
        dets = detector(img)
        shape = None
        height, width, channels = img.shape

        for k, d in enumerate(dets):
            shape = predictor(img, d)

            if(not shape):
                return

            pointList = []
            c = 0
            for b in range(68):
                # sanitizing input points
                point = Point(shape.part(b).x, shape.part(b).y)
                points_data[c] = [point.x, point.y]
                c = c + 1
                # some points might be out of bound
                # so, move them to the closest boundary
                if(point.x < 0):
                    point.x = 0
                elif(point.x >= width):
                    point.x = width - 1
                if(point.y < 0):
                    point.y = 0
                elif(point.y >= height):
                    point.y = height - 1

                pointList.append(point)

            roll = findRoll(pointList)
            #print("roll is " + str(roll) + ' angles')
            yaw = findYaw(pointList)
            #print("yaw is " + str(yaw) + ' angles')
            pitch = findPitch(pointList)
            #print("pitch is " + str(pitch) + ' angles')
            calculateProportion(pointList)
            self.data[frame_number] = [roll, yaw, pitch]
            counter = 0
            for point in pointList:
                cv2.circle(img, (point.x, point.y), ImageProcessor.POINT_SIZE, ImageProcessor.POINT_COLOR, -1)
                counter = counter + 1

            self.draw_triangles(img, pointList)
            
            for pupil in pupils:
                cv2.circle(img, (pupil.left.x, pupil.left.y), 5, (0,0,255), -1)
                cv2.circle(img, (pupil.right.x, pupil.right.y), 5, (0,0,255), -1)
                #points_data[-1] = [pupil.left.x, pupil.left.y]
                #points_data[-2] = [pupil.right.x, pupil.right.y]
                print(pupil.left.x, ", ", pupil.left.y)
                print(pupil.right.x, ", ", pupil.right.y)

            cv2.imwrite(pic_path, img)

    def draw_delaunay(self, img, subdiv):
        """
        """
        triangleList = subdiv.getTriangleList()
        count = 0
        height, width, channels = img.shape
        for triangle in triangleList:
            # first element is x
            # second element is y
            p1 = (triangle[0], triangle[1])
            p2 = (triangle[2], triangle[3])
            p3 = (triangle[4], triangle[5])
            triangle = [p1, p2, p3]
            draw = True
            for p in triangle:
                if(p[0] < 0 or  p[0] >= width or p[1] < 0 or p[1] >= height):
                    draw = False
                    break

            if(draw):
                cv2.line(img, p1, p2, ImageProcessor.POINT_COLOR, 1, 8, 0)
                cv2.line(img, p1, p3, ImageProcessor.POINT_COLOR, 1, 8, 0)
                cv2.line(img, p3, p2, ImageProcessor.POINT_COLOR, 1, 8, 0)



    def draw_triangles(self, img, points):
        """
        """
        shmoints = []
        size = img.shape
        rect = (0, 0, size[1], size[0])
        # Create an instance of Subdiv2D
        subdiv = cv2.Subdiv2D(rect);
        counter = 0
        for p in points:
            subdiv.insert((p.x, p.y))
            counter = counter + 1

        self.draw_delaunay(img, subdiv)

    def drop_data(self, base_name, data):
        #global CURRENT_THREAD_NUM
        #name = 'data' + str(CURRENT_THREAD_NUM) + '.json'
        name = base_name + str(self.index) + '.json'
        print("name of the files is " + str(name))
        with open(os.path.join(self.path_to_pics, name), 'w+') as outfile:
            json.dump(data, outfile)

def merge_jsons(path_to_jsons, base_name):
    path1 = os.path.join(path_to_jsons, base_name + '1.json')
    path2 = os.path.join(path_to_jsons, base_name + '2.json')
    path3 = os.path.join(path_to_jsons, base_name + '3.json')
    path4 = os.path.join(path_to_jsons, base_name + '4.json')
    final_path = os.path.join(path_to_jsons, base_name + '.json')
    with open(path1) as f1, open(path2) as f2,\
         open(path3) as f3, open(path4) as f4:
        first_list = json.load(f1)
        #print(len(first_list))
        second_list = json.load(f2)
        #print(len(second_list))
        third_list = json.load(f3)
        #print(len(third_list))
        fourth_list = json.load(f4)
        #print(len(fourth_list))
    os.unlink(path1)
    os.unlink(path2)
    os.unlink(path3)
    os.unlink(path4)
    z = {**first_list, **second_list, **third_list, **fourth_list}
    with open(final_path, 'w+') as outfile:
        json.dump(z, outfile)

def global_process(path_to_pics, base_name, extension, step_size):
    global CURRENT_THREAD_NUM
    start_time = time.time()
    begin = 1
    following = begin + step_size
    processList = []
    print("Starting to process images using multithreading.\n")
    for i in range(0, THREADS_NUM):
        #last thread should take the rest of the photos.
        if(i == 3):
            following = following + 4
        print("Process " + str(i) + " has started")
        #print("Process " + str(i) + " has started")
        #CURRENT_THREAD_NUM = i + 1

        print("current thread num is " + str(i + 1))
        reader = ImageProcessor(path_to_pics, base_name, extension, i + 1)
        print("Thread " + str(i) + " passing begin index " + str(begin) + " and end " + str(following) + '\n')

        proc = Process(target = reader.process_images, args = (begin, following,))
        processList.append(proc)
        begin = begin + step_size
        following = begin + step_size
        #print("\n")
        proc.start()

    for p in processList:
        p.join()
    elapsed_time = time.time() - start_time
    merge_jsons(path_to_pics, 'data')
    merge_jsons(path_to_pics, 'points')
    print("I am all done waiting for threads, parallel execution took %s seconds.\n" % str(elapsed_time))


def findRoll(pts):
    # points 7 and 33 are the ones that will help determine the angle
    #   B(upNose)   D(projection of B on y axis)
    #
    #
    #
    #               A(chin)
    #
    upNose = pts[33]
    chin = pts[7]
    #
    yDif = abs(upNose.y - chin.y) # AD
    xDif = abs(upNose.x - chin.x) # BD
    gipot = math.sqrt(yDif**2 + xDif**2) #AB
    roll = np.arcsin(xDif/gipot)
    if(upNose.x < chin.x):
        roll = roll * -1

    # from radians to degrees
    return roll*57.2958

def findYaw(pts):#, verbose):
    leftPt = pts[0]
    leftTear = pts[39]
    rightPt = pts[16]
    rightTear = pts[42]

    leftSpan = Point(leftTear.x - leftPt.x, leftTear.y - leftPt.y)
    rightSpan = Point(rightPt.x - rightTear.x, rightPt.y - rightTear.y)

    leftSpanMag = math.sqrt(leftSpan.x**2 + leftSpan.y**2)
    rightSpanMag = math.sqrt(rightSpan.x**2 + rightSpan.y**2)

    deltaSpanMag = leftSpanMag - rightSpanMag
    avgSpanMag = (leftSpanMag + rightSpanMag) / 2
    yaw = deltaSpanMag / avgSpanMag
    yaw *= 180 / np.pi
    return yaw

def findPitch(pts):#, verbose):
    coef = calculateProportion(pts)
    result = 1
    #if(coef < PROPORTION):
    #    result = -1
    t = (coef - PROPORTION)*155
    if(t > 45 or t < -45):
        t = 25*t/abs(t)
    return t


def calculateProportion(pts):
    eyeLine = pts[15].x - pts[19].x
    jawline = math.sqrt((pts[14].x-pts[7].x)**2 + (pts[14].y-pts[7].y)**2)
    #print("proportion is " + str(jawline/eyeLine))
    return jawline/eyeLine

if __name__ == "__main__":
    start_time = time.time()
    # reader = ImageProcessor('/home/andrey/test', 'pic', 'jpg')
    # reader.process_images(1,12)
    # elapsed_time = time.time() - start_time
    # drop_data('/home/andrey/test')
    # print("Sequential execution took %s seconds" % str(elapsed_time))
    reader = ImageProcessor('/Users/temp/projects/CS160/backend/facefinder/core/eyeLike/data', 'pic', 'jpg')
    reader.process_images(1,2)
    elapsed_time = time.time() - start_time
    print("Sequential execution took %s seconds" % str(elapsed_time))
