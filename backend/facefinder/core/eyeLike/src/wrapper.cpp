#include <Python.h>
#include <string>
#include <iostream>
#include <sstream>

#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <queue>
#include <stdio.h>
#include <math.h>
#include <vector>

#include "constants.h"
#include "findEyeCenter.h"
#include "findEyeCorner.h"


using namespace std;

/** Function Headers */
std::string detectAndDisplay( cv::Mat frame );

/** Global variables */
//-- Note, either copy these two files from opencv/data/haarscascades to your current folder, or change these locations
cv::String face_cascade_name = "/root/facefinder68/backend/facefinder/core/eyeLike/res/haarcascade_frontalface_alt.xml";
//cv::String face_cascade_name = "/Users/RYaryy/Desktop/Fall2017/CS160/CS160/backend/facefinder/core/eyeLike/res/haarcascade_frontalface_alt.xml";
//cv::String face_cascade_name = "/Users/temp/projects/CS160/backend/facefinder/core/eyeLike/res/haarcascade_frontalface_alt.xml";
cv::CascadeClassifier face_cascade;
std::string main_window_name = "Capture - Face detection";
std::string face_window_name = "Face Window";
cv::RNG rng(12345);
cv::Mat debugImage;
cv::Mat skinCrCbHist = cv::Mat::zeros(cv::Size(256, 256), CV_8UC1);





std::string findEyes(cv::Mat frame_gray, cv::Rect face) {
  cv::Mat faceROI = frame_gray(face);
  cv::Mat debugFace = faceROI;
  std::ostringstream ss;

  if (kSmoothFaceImage) {
    double sigma = kSmoothFaceFactor * face.width;
    GaussianBlur( faceROI, faceROI, cv::Size( 0, 0 ), sigma);
  }
  //-- Find eye regions and draw them
  int eye_region_width = face.width * (kEyePercentWidth/100.0);
  int eye_region_height = face.width * (kEyePercentHeight/100.0);
  int eye_region_top = face.height * (kEyePercentTop/100.0);

  cv::Rect leftEyeRegion(face.width*(kEyePercentSide/100.0),
                         eye_region_top,eye_region_width,eye_region_height);

  cv::Rect rightEyeRegion(face.width - eye_region_width - face.width*(kEyePercentSide/100.0),
                          eye_region_top,eye_region_width,eye_region_height);

  //-- Find Eye Centers
  cv::Point leftPupil = findEyeCenter(faceROI,leftEyeRegion,"Left Eye");
  cv::Point rightPupil = findEyeCenter(faceROI,rightEyeRegion,"Right Eye");

  // get corner regions
  cv::Rect leftRightCornerRegion(leftEyeRegion);
  leftRightCornerRegion.width -= leftPupil.x;
  leftRightCornerRegion.x += leftPupil.x;
  leftRightCornerRegion.height /= 2;
  leftRightCornerRegion.y += leftRightCornerRegion.height / 2;
  cv::Rect leftLeftCornerRegion(leftEyeRegion);
  leftLeftCornerRegion.width = leftPupil.x;
  leftLeftCornerRegion.height /= 2;
  leftLeftCornerRegion.y += leftLeftCornerRegion.height / 2;
  cv::Rect rightLeftCornerRegion(rightEyeRegion);
  rightLeftCornerRegion.width = rightPupil.x;
  rightLeftCornerRegion.height /= 2;
  rightLeftCornerRegion.y += rightLeftCornerRegion.height / 2;
  cv::Rect rightRightCornerRegion(rightEyeRegion);
  rightRightCornerRegion.width -= rightPupil.x;
  rightRightCornerRegion.x += rightPupil.x;
  rightRightCornerRegion.height /= 2;
  rightRightCornerRegion.y += rightRightCornerRegion.height / 2;
  
  // std::cout << face.x << " " << face.y << " " << face.width << std::endl;
  // std::cout << leftEyeRegion.x << " " << leftEyeRegion.y << " " << leftEyeRegion.width << std::endl;
  // std::cout << leftRightCornerRegion.x << " " << leftRightCornerRegion.y << " " << leftRightCornerRegion.width << std::endl;
  // std::cout << leftLeftCornerRegion.x << " " << leftLeftCornerRegion.y << " " << leftLeftCornerRegion.width << std::endl;
  // std::cout << rightEyeRegion.x << " " << rightEyeRegion.y << " " << rightEyeRegion.width << std::endl; 
  // std::cout << rightLeftCornerRegion.x << " " << rightLeftCornerRegion.y << " " << rightLeftCornerRegion.width << std::endl;
  // std::cout << rightRightCornerRegion.x << " " << rightRightCornerRegion.y << " " << rightRightCornerRegion.width << std::endl;
  // std::cout << eye_region_width << std::endl;
/*
391 103 369
47 92 129
119 119 57
47 119 72
192 92 129
192 119 62
254 119 67
129
*/
  // change eye centers to face coordinates
  rightPupil.x  +=  rightEyeRegion.x  + face.x;
  rightPupil.y  +=  rightEyeRegion.y  + face.y;
  leftPupil.x   +=  leftEyeRegion.x   + face.x;
  leftPupil.y   +=  leftEyeRegion.y   + face.y;
  // flip the coordinates along x-axis
  int halfwidth = frame_gray.cols / 2;
  
  // on right side
  if (rightPupil.x > halfwidth){
    int delta = rightPupil.x - halfwidth;
    rightPupil.x = halfwidth - delta;
  } else{ // on left side
    int delta = halfwidth - rightPupil.x;
    rightPupil.x = halfwidth + delta;
  }
  if (leftPupil.x > halfwidth){
    int delta = leftPupil.x - halfwidth;
    leftPupil.x = halfwidth - delta;
  } else{ // on left side
    int delta = halfwidth - leftPupil.x;
    leftPupil.x = halfwidth + delta;
  }

  // draw eye centers
  //circle(faceROI, leftPupil, 3, 0);
  //circle(faceROI, rightPupil, 3, 0);
  ss << leftPupil.x  << "," <<  leftPupil.y   << ";";
  ss << rightPupil.x << "," <<  rightPupil.y  << "/";

  

  //-- Find Eye Corners
  if (kEnableEyeCorner) {
    cv::Point2f leftRightCorner = findEyeCorner(faceROI(leftRightCornerRegion), true, false);
    leftRightCorner.x += leftRightCornerRegion.x;
    leftRightCorner.y += leftRightCornerRegion.y;
    cv::Point2f leftLeftCorner = findEyeCorner(faceROI(leftLeftCornerRegion), true, true);
    leftLeftCorner.x += leftLeftCornerRegion.x;
    leftLeftCorner.y += leftLeftCornerRegion.y;
    cv::Point2f rightLeftCorner = findEyeCorner(faceROI(rightLeftCornerRegion), false, true);
    rightLeftCorner.x += rightLeftCornerRegion.x;
    rightLeftCorner.y += rightLeftCornerRegion.y;
    cv::Point2f rightRightCorner = findEyeCorner(faceROI(rightRightCornerRegion), false, false);
    rightRightCorner.x += rightRightCornerRegion.x;
    rightRightCorner.y += rightRightCornerRegion.y;
    // circle(faceROI, leftRightCorner, 3, 100);
    // circle(faceROI, leftLeftCorner, 3, 500);
    // circle(faceROI, rightLeftCorner, 3, 200);
    // circle(faceROI, rightRightCorner, 3, 200);
  }
  // imshow(face_window_name, faceROI);
  return ss.str();
}


cv::Mat findSkin (cv::Mat &frame) {
  cv::Mat input;
  cv::Mat output = cv::Mat(frame.rows,frame.cols, CV_8U);

  cvtColor(frame, input, CV_BGR2YCrCb);

  for (int y = 0; y < input.rows; ++y) {
    const cv::Vec3b *Mr = input.ptr<cv::Vec3b>(y);
//    uchar *Or = output.ptr<uchar>(y);
    cv::Vec3b *Or = frame.ptr<cv::Vec3b>(y);
    for (int x = 0; x < input.cols; ++x) {
      cv::Vec3b ycrcb = Mr[x];
//      Or[x] = (skinCrCbHist.at<uchar>(ycrcb[1], ycrcb[2]) > 0) ? 255 : 0;
      if(skinCrCbHist.at<uchar>(ycrcb[1], ycrcb[2]) == 0) {
        Or[x] = cv::Vec3b(0,0,0);
      }
    }
  }
  return output;
}


std::string detectAndDisplay( cv::Mat frame ) {
  std::vector<cv::Rect> faces;
  std::string eyes = "";

  std::vector<cv::Mat> rgbChannels(3);
  cv::split(frame, rgbChannels);
  cv::Mat frame_gray = rgbChannels[2];

  //-- Detect faces
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, cv::Size(150, 150) );
  //std::cout << "Number of Faces found: " << faces.size() << std::endl;
  for( int i = 0; i < faces.size(); i++ ){
    rectangle(debugImage, faces[i], 1234);
  }
  for (int i = 0; i < faces.size() ; i++){
  	eyes += findEyes(frame_gray, faces[i]);
  }
  return eyes;
}



extern "C"
const char *eyes_in_video(char* name){
	std::string all_eyes = "";
	//cout<<strlen(name)<<endl;
	//cout<<name<<endl;

  	createCornerKernels();
  	ellipse(skinCrCbHist, cv::Point(113, 155.6), cv::Size(23.4, 15.2),
          43.0, 0.0, 360.0, cv::Scalar(255, 255, 255), -1);

	cv::Mat frame;
	std::string videofilename = std::string(name);
	if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading face cascade, please change face_cascade_name in source code.\n"); return "0"; };
	  // I make an attempt at supporting both 2.x and 3.x OpenCV

  	cv::VideoCapture capture(videofilename);
  	if( capture.isOpened() ) {
	    while( true ) {
		    capture.read(frame);

			cv::flip(frame, frame, 1);
			frame.copyTo(debugImage);
			if( !frame.empty() ) {
	        	all_eyes += detectAndDisplay( frame );
	        	all_eyes += "F";
	      	}
	      	else {
	        	printf(" --(!) No captured frame -- Break!");
	        	break;
	      	}
		}
	}
	return all_eyes.c_str();
}




extern "C"
const char *eyes_in_picture(char* name){
	std::string eyes_in_frame = "";

  	createCornerKernels();
  	ellipse(skinCrCbHist, cv::Point(113, 155.6), cv::Size(23.4, 15.2),
          43.0, 0.0, 360.0, cv::Scalar(255, 255, 255), -1);

	cv::Mat frame;
	std::string imagefilename = std::string(name);
	frame = cv::imread(imagefilename, CV_LOAD_IMAGE_COLOR);

	if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading face cascade, please change face_cascade_name in source code.\n"); return "0"; };
	  // I make an attempt at supporting both 2.x and 3.x OpenCV


	cv::flip(frame, frame, 1);
	frame.copyTo(debugImage);
	if( !frame.empty() ) {
    	eyes_in_frame += detectAndDisplay( frame );
  	}
  	else {
    	printf(" --(!) No captured frame -- Break!");
  	}

	return eyes_in_frame.c_str();
}

