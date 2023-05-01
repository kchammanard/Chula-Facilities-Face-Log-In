import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import numpy as np
from datetime import datetime
from collections.abc import MutableMapping
from pymongo.mongo_client import MongoClient
import hashlib

cluster = ""
client = MongoClient(cluster)

db = client.facedb
student_collection = db.students
face_collection = db.face
facility_collection = db.facility
activity_collection = db.activity
entry_collection = db.entry

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

hashed = []
for my_list in encodeListKnown:
    list_string = str(my_list)
    hash_object = hashlib.sha1(list_string.encode())
    hex_digest = hash_object.hexdigest()
    unique_integer = int(hex_digest, 16)%1000000
    hashed.append(unique_integer)
print(hashed)

modeType = 0
counter = 0
id = -1
imgStudent = []

def choose_facility():
    while True:
        img = cv2.imread('Resources/facilities.jpg')
        img = cv2.resize(img, (1280,720))
        cv2.imshow("Choose Facility", img)

        key = cv2.waitKey(1)

        if key == ord('a'):
            return 1001
        if key == ord('b'):
            return 1002
        if key == ord('c'):
            return 1003

def main():
    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        # imgBackground[162:162 + 480, 55:55 + 640] = img
        # imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)
                # print("Match Index", matchIndex)

                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(studentIds[matchIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = x1, y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(img, bbox, rt=0)
                    id = studentIds[matchIndex]
                    if counter == 0:
                        #print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                        cvzone.putTextRect(img, "Loading", (200, 240))
                        cv2.imshow("Face", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

            if counter != 0:
                if counter == 1:
                    card = cv2.imread("Resources/output.jpg")
                    card = cv2.resize(card, (500,700))
                    
                    face_id = hashed[matchIndex]

                    first_name = student_collection.find_one({"face_id": face_id})["f_name"]
                    last_name = student_collection.find_one({"face_id": face_id})["l_name"]
                    student_id = student_collection.find_one({"face_id": face_id})["student_id"]
                    faculty = student_collection.find_one({"face_id": face_id})["faculty"]

                    if matches[matchIndex]:
                        prof = cv2.imread(f'Profile Images/{student_id}.jpg')
                        prof_resized = cv2.resize(prof, (158,178))

                        card[350-180:528-180,172:330] = prof_resized

                    entry_id = activity_collection.find_one({"face_id": face_id,"facility_id":chosen_facility_id})["entry_id"]
                    
                    entry = entry_collection.find_one({"entry_id": entry_id})["can_enter"]

                    name = f"{first_name} {last_name}"
                    text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    text_size2, _ = cv2.getTextSize(facility, cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)

                    cv2.putText(card, facility, (int(250 - text_size2[0]/2), 390), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
                    cv2.putText(card, name, (int(250 - text_size[0]/2), 430), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                    cv2.putText(card, str(student_id), (200,480), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                    cv2.putText(card, faculty, (200,505), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

                    if entry:
                        cv2.putText(card, "Allowed", (200,530), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 1)
                    else:
                        cv2.putText(card, "Not Allowed", (200,530), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 1)
                        cv2.putText(card, entry_collection.find_one({"entry_id": entry_id})["reason"], (200,555), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                        #print("Rejected:", entry_collection.find_one({"entry_id": entry_id})["reason"])

                    cv2.imshow(facility, card)

        else:
            modeType = 0
            counter = 0
            # if cv2.getWindowProperty(facility, cv2.WND_PROP_VISIBLE) < 1:
            #     cv2.destroyWindow(facility)
        # cv2.imshow("Webcam", img)
        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__test__":
    chosen_facility_id = choose_facility()
    facility = facility_collection.find_one({"facility_id": chosen_facility_id})["facility_name"]
    print(chosen_facility_id)
    cv2.destroyAllWindows()
