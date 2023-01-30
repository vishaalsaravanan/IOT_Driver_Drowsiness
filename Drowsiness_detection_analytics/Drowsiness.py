from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import pyttsx3
import numpy as np
from random import randint
import time
import firebase_admin
from firebase_admin import db,auth
from PyQt5.QtWidgets import  QInputDialog, QLineEdit, QApplication
from PyQt5.QtCore import QCoreApplication
import pyrebase


#password prompt dialog box 
def prompt_password(user):

    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])

    text, ok = QInputDialog.getText(
        None,
        "Credential",
        "user {}:".format(user),
        QLineEdit.Password)
    if ok and text:
        return text
    raise ValueError("Must specify a valid password")

# fetching existing user 
def existing_user():
    email=input("Email Id:")
    password=prompt_password(email)
    auth=firebase.auth()
    signin=auth.sign_in_with_email_and_password(email,password)
    user_uid=signin['idToken']
    user_detail=auth.get_account_info(user_uid)
    userid=user_detail['users']
    local_id=userid[0]['localId']
    user_uid=local_id
    #updating new values in database

    
    return local_id #return uid of the signed user

#adding new user 
def create_user():
    email=input("Email Id:")
    password=prompt_password(email)
    user=auth.create_user(email=email,password=password)
    print("User Added successfully ")
    user_id=user.uid
       # Initializing dummy variables
    yawn={}
    blink={}
    drowsiness={}
    val=1
    yawn["a"]=val
    blink["a"]=val
    drowsiness["a"]=val
    current_total_yawns=0 #maximum yawn in single program run
    current_total_blinks=0 #maximum yawn in single program run
    current_total_drowsiness=0 #maximum yawn in single program run(a.k.a "Single Critical Alert")
    trips=0
    n = input("Enter your name")
    #Storing root structure in the database
    data={"yawns":yawn,
        "blinks":blink,
        "drowsiness":drowsiness,
        "total_yawns":current_total_yawns,
        "totaldrowsiness":current_total_drowsiness,
        "total_blink":current_total_blinks,
        "trips":trips,
        "name": n}
    ref = db.reference("/").child(user_id)
    red=ref.set(data)
    return user_id #return uid of the signed user

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_landmarks(im):
    rects = detector(im, 1)
    if len(rects) > 1:
        return "error"
    if len(rects) == 0:
        return "error"
    return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])


def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im

def top_lip(landmarks):
    top_lip_pts = []
    for i in range(50,53):
        top_lip_pts.append(landmarks[i])
    for i in range(61,64):
        top_lip_pts.append(landmarks[i])
    top_lip_all_pts = np.squeeze(np.asarray(top_lip_pts))
    top_lip_mean = np.mean(top_lip_pts, axis=0)
    return int(top_lip_mean[:,1])

def bottom_lip(landmarks):
    bottom_lip_pts = []
    for i in range(65,68):
        bottom_lip_pts.append(landmarks[i])
    for i in range(56,59):
        bottom_lip_pts.append(landmarks[i])
    bottom_lip_all_pts = np.squeeze(np.asarray(bottom_lip_pts))
    bottom_lip_mean = np.mean(bottom_lip_pts, axis=0)
    return int(bottom_lip_mean[:,1])

def mouth_open(image):
    landmarks = get_landmarks(image)
    
    if landmarks == "error":
        return image, 0
    
    image_with_landmarks = annotate_landmarks(image, landmarks)
    top_lip_center = top_lip(landmarks)
    bottom_lip_center = bottom_lip(landmarks)
    lip_distance = abs(top_lip_center - bottom_lip_center)
    return image_with_landmarks, lip_distance

if __name__=="__main__":
   config=  {
                    
                "apiKey": "AIzaSyC_9MN-e2kLYGoXEa-ujZhMJ5KEDhxrxv0",
                "authDomain": "drowsi-6f166.firebaseapp.com",
                "databaseURL": "https://drowsi-6f166-default-rtdb.firebaseio.com",
                "projectId": "drowsi-6f166",
                "storageBucket": "drowsi-6f166.appspot.com",
                "messagingSenderId": "198177358258",
                "appId": "1:198177358258:web:220473766070b40a1224ab",
                "measurementId": "G-FD48W8GKN9"
                }
    
   if not firebase_admin._apps:
       cred_obj = firebase_admin.credentials.Certificate('serviceAccountKey.json')
       default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': 'https://drowsi-6f166-default-rtdb.firebaseio.com/'})
       firebase=pyrebase.initialize_app(config)
    
   user_type=int(input("\n1.New User \n2.Existing User\n"))
   if user_type==1:
        user_id=create_user()
   else:
        user_id=existing_user()
        
   
   #Fetching existing Data from the firebase
   existing_data=db.reference("/").child(user_id).get()
    # print(existing_data)
    # fetching and storing child node values
   existing_blinks={}
   existing_blinks=existing_data['blinks']
   existing_yawns=existing_data['yawns']
   existing_drowsiness=existing_data['drowsiness']
   total_blink=existing_data['total_blink']
   total_yawns=existing_data['total_yawns']
   total_drowsiness=existing_data['totaldrowsiness']
   trips=existing_data['trips']
   
   drowsiness_counter=0
   engine = pyttsx3.init()
   engine.say("Alert System Activated")
   engine.runAndWait()    
   thresh = 0.25
   frame_check = 20
   detect = dlib.get_frontal_face_detector()
   predict = dlib.shape_predictor(".\shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
   PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
   predictor = dlib.shape_predictor(PREDICTOR_PATH)
   detector = dlib.get_frontal_face_detector()
   (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
   (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
   cap=cv2.VideoCapture(0)
   flag=0
   yawns = 0
   yawn_status = False 
   blink=0
    
   while True:
        ret, frame=cap.read()
        frame = imutils.resize(frame, width=450)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        
        image_landmarks, lip_distance = mouth_open(frame)   
        prev_yawn_status = yawn_status  
        if lip_distance > 15:
            yawn_status = True 
            cv2.putText(frame, "Subject is Yawning", (50,450), 
                        cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),2)
            
    
            output_text = " Yawn Count: " + str(yawns + 1)
    
            cv2.putText(frame, output_text, (50,50),
                        cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)
            
        else:
            yawn_status = False 
             
        if prev_yawn_status == True and yawn_status == False:
            yawns += 1
            time_stamp=int(time.time())
            existing_yawns[time_stamp]=yawns
            
        
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)#converting to NumPy Array
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < thresh:
                flag += 1
                if flag >= frame_check:
                    cv2.putText(frame, "****************ALERT!****************", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "****************ALERT!****************", (10,325),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    engine.say("Crictical Alert: Stop The Car")
                    blink=blink+1
                    time_stamp=int(time.time())
                    existing_blinks[time_stamp]=blink
                    engine.runAndWait() 
    
            else:
                flag = 0
        if yawn_status == True and flag == 1:
            oxygen=randint(88,95)
            cv2.putText(frame, "O2 level: {} %".format(oxygen), (40, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        else:
            oxygen=randint(95,101)
            cv2.putText(frame, "O2 level: {} %".format(oxygen), (40, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if blink>1 and yawns>1:
            drowsiness_counter=5
            engine.say("Extreme Alert: Hazard Mode Activated !")
            engine.runAndWait() 
            engine.say("CAR Engine OFF")
            engine.runAndWait() 
            cap.release()
            cv2.destroyAllWindows()
            #Updating in firebase 
            time_stamp=int(time.time())
            existing_drowsiness[time_stamp]=existing_drowsiness+1
            total_yawns=total_yawns+yawns
            total_blink=total_blink+blink
            trips=trips+1
            total_drowsiness=total_drowsiness+1
            data={"yawns":existing_yawns,
        "blinks":existing_blinks,
        "drowsiness":existing_drowsiness,
        "total_yawns":total_yawns,
        "totaldrowsiness":total_drowsiness,
        "total_blink":total_blink,
        "trips":trips}
            update_data = db.reference("/").child(user_id)
            red=update_data.update(data)     
            break
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
    
            break
   cap.release()
   cv2.destroyAllWindows()