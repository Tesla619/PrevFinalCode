import time
from turtle import distance
import tensorflow as tf
import cv2
import numpy as np
#from PIL import Image
from object_detection.utils import label_map_util
#from object_detection.utils import visualization_utils as viz_utils
#from base64 import b64encode

PATH_TO_SAVED_MODEL = "customTF2/data/inference_graph/saved_model"

Known_distance = 223
Known_width    = 35 #109 pixels

# Load label map and obtain class names and ids
category_index=label_map_util.create_category_index_from_labelmap("customTF2/data/label_map.pbtxt",use_display_name=True)

def visualise_on_image(image, bboxes, labels, scores, thresh):
    (h, w, d) = image.shape
    for bbox, label, score in zip(bboxes, labels, scores):
        if score > thresh:
            xmin, ymin = int(bbox[1]*w), int(bbox[0]*h)
            xmax, ymax = int(bbox[3]*w), int(bbox[2]*h)

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0,255,0), 2)
            cv2.putText(image, f"{label}: {int(score*100)} %", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                        
            #cv2.putText(frame, "xmin: " + str(xmin) + " xmax: " + str(xmax) + " ymin: " + str(ymin) + " ymax: " + str(ymax), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)    
    return image

def coord(image, bboxes, labels, scores, thresh):
    (h, w, d) = image.shape
    for bbox, label, score in zip(bboxes, labels, scores):
        if score > thresh:
            xmin, ymin = int(bbox[1]*w), int(bbox[0]*h)
            xmax, ymax = int(bbox[3]*w), int(bbox[2]*h)            
            return xmin, xmax, ymin, ymax
        else: return 0,0,0,0

def width(image, bboxes, labels, scores, thresh):
    (h, w, d) = image.shape
    for bbox, label, score in zip(bboxes, labels, scores):
        if score > thresh:
            xmin, ymin = int(bbox[1]*w), int(bbox[0]*h)
            xmax, ymax = int(bbox[3]*w), int(bbox[2]*h)                        
            return (xmax - xmin)
        else: return 0 #1 to not cause non div error

# focal length finder function

def FocalLength(measured_distance, real_width, width_in_rf_image): 
    focal_length = (width_in_rf_image* measured_distance)/ real_width
    return focal_length

#camera at height of 80-90 84cm
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length)/face_width_in_frame
    return distance
   
    
if __name__ == '__main__':
    
    # Load the model
    print("Loading saved model ...")
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    print("Model Loaded!")
    
    # Video Capture (video_file)
    #video_capture = cv2.VideoCapture("input.mp4")
    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    #fps = int(video_capture.get(5))
    size = (frame_width, frame_height)
    
    #Initialize video writer
    result = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'MJPG'),15, size)

    #-----Ref Data Gathering-------
    ref_image = cv2.imread("ref_images/ref1.jpg")
    ref_image_face_width = 109#width(ref_image)
    focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
    print("Focal Length of Ref: ",focal_length_found)
    #cv2.imshow("ref_image", ref_image)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print('Unable to read video / Video ended')
            break
    
        frame = cv2.flip(frame, 1)
        image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        # The model expects a batch of images, so also add an axis with `tf.newaxis`.
        input_tensor = tf.convert_to_tensor(image_np)[tf.newaxis, ...]

        # Pass frame through detector
        detections = detect_fn(input_tensor)

        # Set detection parameters
        score_thresh = 0.4   # Minimum threshold for object detection
        max_detections = 1

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        scores = detections['detection_scores'][0, :max_detections].numpy()
        bboxes = detections['detection_boxes'][0, :max_detections].numpy()
        labels = detections['detection_classes'][0, :max_detections].numpy().astype(np.int64)
        labels = [category_index[n]['name'] for n in labels]

        # Display detections
        visualise_on_image(frame, bboxes, labels, scores, score_thresh)
        #-------------------------------------------------------------------------------------
        
        #if not coord(frame, bboxes, labels, scores, score_thresh) == (0,0,0,0):
            #print(coord(frame, bboxes, labels, scores, score_thresh))
            
        # if not width(frame, bboxes, labels, scores, score_thresh) == 0:
        #     print("Width: ", width(frame, bboxes, labels, scores, score_thresh))        
        
        # measured_distance = 223           
        # real_width = 35         #width of robot wheel to wheel
        # real_face_width = 35    #width of robot wheel to wheel #may need to replace this for another value
        
        # face_width_in_frame = width(frame, bboxes, labels, scores, score_thresh)
        # width_in_rf_image   = 136#width(frame, bboxes, labels, scores, score_thresh) #need to fix this
                
        # Focal_Length = FocalLength(measured_distance, real_width, width_in_rf_image)
        # Distance = Distance_finder(Focal_Length, real_face_width, face_width_in_frame)
        
        # print("Focal Length: ", Focal_Length)
        # print("Distance: ", Distance)        
        
        # calling face_data function
        face_width_in_frame = width(frame, bboxes, labels, scores, score_thresh)
        # finding the distance by calling function Distance
        if face_width_in_frame != 0:
            Distance = Distance_finder(focal_length_found, Known_width, face_width_in_frame)
            # Drwaing Text on the screen
            cv2.putText(frame, f"Distance: {Distance} cm", (frame_width - 270, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)        
        
        #-------------------------------------------------------------------------------------
        end_time = time.time()
        fps = int(1/(end_time - start_time))
        start_time = end_time
        
        #cv2.imwrite("images/ref1.jpg",frame)
        
        cv2.putText(frame, f"FPS: {fps}", (20,frame_height-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        #cv2.putText(frame, f"BoxWidth: {face_width_in_frame}", (frame_width - 250, frame_height - 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        #cv2.putText(frame, f"Focal  L: {Focal_Length}", (frame_width - 250, frame_height - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        
        
        #cv2.imwrite("images/ref2.jpg",frame)
        
        #Write output video
        result.write(frame)
      
        cv2.imshow("Results", frame)
        
        key = cv2.waitKey(1) & 0XFF
        if key == ord("q"):
            break

    video_capture.release()