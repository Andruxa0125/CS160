import dlib
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from multiprocessing import Process
import time

#TODO: change this path to something coooool
predictor_path = "/Users/RYaryy/Desktop/Fall2017/CS160/CS160/backend/static/shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

THREADS_NUM = 4
STEP_SIZE = 1

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
    def __init__(self, path_to_pics, base_name, extension):
        self.path_to_pics = path_to_pics
        self.base_name = base_name
        self.ext = extension

    def process_images(self, beginIndex, endIndex):
        for num in range(beginIndex, endIndex):
            pic_name = self.base_name + str(num) + '.' + self.ext
            #print(pic_name)
            pic_path = os.path.join(self.path_to_pics, pic_name)
            #print(pic_path)
            self.draw_points(pic_path)

    def draw_points(self, pic_path):
        """
        Takes a picture, detects a face and draws all the points.
        args: a full path to the picture
        """
        img = cv2.imread(pic_path)
        #print (pic_path)
        #print(os.path.exists(pic_path))
        dets = detector(img)
        shape = None
        height, width, channels = img.shape

        for k, d in enumerate(dets):
            shape = predictor(img, d)

        if(not shape):
            return

        pointList = []
        for b in range(68):
            point = Point(shape.part(b).x, shape.part(b).y)
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

        counter = 0
        for point in pointList:         
            cv2.circle(img, (point.x, point.y), ImageProcessor.POINT_SIZE, ImageProcessor.POINT_COLOR, -1)
            counter = counter + 1

        self.draw_triangles(img, pointList)  

        cv2.imwrite(pic_path, img)

    def draw_delaunay(self, img, subdiv):
        """
        """
        triangleList = subdiv.getTriangleList();
        count = 0
        height, width, channels = img.shape
        for triangle in triangleList:
            # first element is x
            # second element is y
            p1 = (triangle[0], triangle[1])
            #print("Point 1 has coordinates %d on x and %d on y" % (p1[0], p1[1]))
            p2 = (triangle[2], triangle[3])
            # print("Point 2 has coordinates %d on x and %d on y" % (p2[0], p2[1]))
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
        #print("I have inserted %s points" % str(counter))

        self.draw_delaunay(img, subdiv)

def global_process(path_to_pics, base_name, extension, step_size): 
    start_time = time.time()
    begin = 1
    following = begin + step_size
    processList = []
    for i in range(0, THREADS_NUM):
        #print("Process " + str(i) + " has started")
        reader = ImageProcessor(path_to_pics, base_name, extension)
        print("thread " + str(i) + "passing begin index " + str(begin) + " and end " + str(following) + '\n')

        proc = Process(target = reader.process_images, args = (begin, following,))
        processList.append(proc)
        begin = begin + step_size
        following = begin + step_size
        #print("\n")
        proc.start()

    for p in processList:
        p.join()
    elapsed_time = time.time() - start_time
    print("I am all done waiting for threads, parallel execution took %s seconds" % str(elapsed_time))

# start_time = time.time()
# reader = ImageProcessor('', 'pic', 'jpg')
# reader.process_images(1,5)
# elapsed_time = time.time() - start_time
# print("Sequential execution took %s seconds" % str(elapsed_time))