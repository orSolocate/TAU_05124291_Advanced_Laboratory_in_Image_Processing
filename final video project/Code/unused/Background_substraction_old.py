from __future__ import print_function
import cv2 as cv
import cv2
import numpy as np
import argparse
import sys


parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='Stabilized_Example_INPUT.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='KNN')
args = parser.parse_args()

## [create]
#create Background Subtractor objects
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:                                                  #was 120                 400
    backSub = cv.createBackgroundSubtractorKNN(history = 120, dist2Threshold = 400.0, detectShadows = True)#eas True
## [create]
#cv.BackgroundSubtractorKNN.setkNNSamples(backSub,50) #How many nearest neighbours need to match.
#cv.BackgroundSubtractorKNN.setNSamples(backSub,1) #Sets the number of data samples in the background model.

## [capture]
capture = cv.VideoCapture('Stabilized_Example_INPUT.avi')#('stabilize.avi')#
#capture = cv.VideoCapture('video_out.avi')
n_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)
## [capture]

# Get width and height of video stream
w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get frames per second (fps)
fps = capture.get(cv2.CAP_PROP_FPS)

# Define the codec for output video
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# Set up output video
out = cv2.VideoWriter('Backgroud_Substraction_out.avi', fourcc, fps, (w, h))
# Set up output video
out_bin = cv2.VideoWriter('binary.avi', fourcc, fps, (w, h))

background_from_median_filter = cv2.imread('background_from_median_filter.jpeg')
iteration= 1
background = cv2.imread('background.jpeg')


while True:
    ret, frame = capture.read()

    if frame is None:
        break

    if iteration==1:
       first_frame = frame


    ##############
    #frame = cv2.medianBlur(frame, 5)
    #frame = cv2.bilateralFilter(frame, 9, 75, 75)
    #cv.imshow('real Frame 1', frame)
    #frame = 255 - cv2.absdiff(frame,background_from_median_filter)
    #cv.imshow('real Frame 2', frame)
    #kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    #frame = cv.filter2D(frame, -1, kernel)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    #frame = cv2.dilate(frame, kernel, iterations=2)  # wider

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame[:, :, 0] = cv.equalizeHist(frame[:, :, 0])
    #frame[:, :, 1] = cv.equalizeHist(frame[:, :, 1])
    #frame[:, :, 2] = cv.equalizeHist(frame[:, :, 2])
    #frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
    #cv.imshow('equalizeHist', frame)

    # convert image from RGB to HSV
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    # Histogram equalisation on the V-channel
    #frame_hsv[:, :, 2] = cv2.equalizeHist(frame_hsv[:, :, 2])
    # convert image back from HSV to RGB
    #frame = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2RGB)

    #unsharp mask
    #gaussian_3 = cv2.GaussianBlur(frame, (25, 25), 10.0)
    #unsharp_image = cv2.addWeighted(frame, 1.5, gaussian_3, -0.5, 0, frame)


    ## [apply]
    #update the background model
    # learningRate = 1 the background model is completely reinitialized from the last frame.
    # learningRate = between 0 and 1 that indicates how fast the background model is learnt.
    # learningRate = -1 some automatically chosen learning rate
    #frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]),int(bbox[0]):int(1.1*(bbox[0]+bbox[2])), : ]

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #frame = cv2.GaussianBlur(frame, (51, 51), 0)

    # In each iteration, calculate absolute difference between current frame and reference frame
    #difference = cv2.absdiff(gray, first_gray)
    fgMask = backSub.apply(frame,learningRate = -1) # learningrate was -1
    #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    ## [apply]

    ## [display_frame_number]
    #get the frame number and write it on the current frame
    #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    #cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
    #           cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    ## [display_frame_number]


    #yonatan's add
    ###############################################################################################
    #if (iteration <= int(n_frames / 4)): # 0 to 1
    #    fgMask[:, int(1.8*1 * fgMask.shape[1]/4):int(4*fgMask.shape[1]/4)]=0

    #if (iteration <= int(2*n_frames / 4) and (iteration >= 1*n_frames/4)): #1 to 2
    #    fgMask[:, int(0 * fgMask.shape[1]/4):int(0.8*1*fgMask.shape[1]/4)]=0
    #    fgMask[:, int(1.4*2 * fgMask.shape[1]/4):int(4*fgMask.shape[1]/4)]=0

    #if (iteration <= 3*n_frames / 4) and (iteration >= 2*n_frames/4): #2 to 3
    #    fgMask[:, int(0 * fgMask.shape[1]/4):int(0.8*2*fgMask.shape[1]/4)]=0
    #    fgMask[:, int(1.4*3 * fgMask.shape[1]/4):int(4*fgMask.shape[1]/4)]=0

    #if (iteration <= 4*n_frames / 4) and (iteration >= 3*n_frames / 4): #3 to 4
    #    fgMask[:, int(0 * fgMask.shape[1]):int(0.8*3* fgMask.shape[1] / 4)]=0
    ##############################################################################################

    #kernel = np.ones((5,5),np.uint8)
    #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    fgMask[fgMask < 254] = 0
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    #fgMask = cv2.erode(fgMask, kernel, iterations=1)  # thiner

    ####amazing results!!!!!!!!!!!!!!
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 10))  # 20,10
    fgMask = cv2.erode(fgMask, kernel, iterations=2)  # thiner 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 5,5
    fgMask = cv2.dilate(fgMask, kernel, iterations=5)  # wider 5
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    # fgMask = cv2.erode(fgMask, kernel, iterations=1)  # thiner
    #################################


#############BLOB DETECTOR- black
    #INVERT MASK
    fgMask = cv2.bitwise_not(fgMask)

   # # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0 #10
    params.maxThreshold = 200 #200

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 0.01#1500
    #params.maxArea = 100

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.01#0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(fgMask)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob

    im_with_keypoints = cv2.drawKeypoints(fgMask, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    for keyPoint in keypoints:
        x = int(keyPoint.pt[0])
        y = int(keyPoint.pt[1])
        s = keyPoint.size#the diameter of the blob
        # Center coordinates
        center_coordinates = (x,y)
        # Radius of circle
        radius = int(s)
        # white color in BGR
        color = (255, 255, 255)

        # Line thickness of 2 px
        thickness = 1

        # Using cv2.circle() method
        # Draw a circle with blue line borders of thickness of 2 px
        if(s<=50):
            fgMask = cv2.circle(fgMask, center_coordinates, radius, color, cv.FILLED) #cv.FILLED



    fgMask = cv2.bitwise_not(fgMask) #invert image to original

    # Show blobs
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)


#############
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 20,10
    #fgMask = cv2.erode(fgMask, kernel, iterations=3)  # thiner 1
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))  # 5,5
    #fgMask = cv2.dilate(fgMask, kernel, iterations=1)  # wider 5


    #fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
    #fgMask[fgMask < 150] = 0

    #fgMask = cv2.bilateralFilter(fgMask, 9, 250, 250)
    #fgMask = cv2.dilate(fgMask, kernel, iterations=4)  # wider

    #fgMask = cv2.medianBlur(fgMask, 21)
    fgMask = fgMask/255
    #frame = fgMask * frame #for grayscale images
    frame[:, :, 0] = fgMask * frame[:, :, 0]
    frame[:, :, 1] = fgMask * frame[:, :, 1]
    frame[:, :, 2] = fgMask * frame[:, :, 2]
    #hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #hsv[:,:,1] = hsv[:,:,1]*fgMask
    #frame = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    #print(frame.shape)  (1080,1920,3)

    ## [show]
    #show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    iteration = iteration + 1
    ## [show]
    if(iteration>=6):
        out.write(frame)
        fgMask = np.uint8(255*fgMask)
        fgMask = cv2.cvtColor(fgMask, cv2.COLOR_GRAY2RGB)
        out_bin.write(fgMask)
    print('processing frame number',iteration)


    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

# Release video
capture.release()
out.release()
out_bin.release()