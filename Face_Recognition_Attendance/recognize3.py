import cv2
import numpy as np
import pandas as pd
import time
from datetime import datetime
from datetime import date
import csv
import sys
import os.path
s


list1=[]
list2=[]
list3=[]
dates1=date.today()
dates=str(dates1)+".csv"
file_exists = os.path.exists(dates)
if not file_exists:
    file = open(dates, 'w+')
    writer = csv.writer(file)
    writer.writerow(['Name', 'Time', 'Date(YYYY-MM-DD)', 'Entry/Exit'])
    file.close()




def markAttendace(name):

    with open(dates,'r+') as f:
        myDataList=f.readlines()
        data=pd.read_csv(dates)

        #print(data)
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        ddate = date.today()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            f.writelines(f'\n{name},{dtString},{ddate},{"entry"}')
            exit()




        else:


            count = 0


            for i in range(0, len(nameList)):
                strname = str(nameList[i])
                if strname == name:
                    count = count + 1



            if (count%2 == 1):
                f.writelines(f'\n{name},{dtString},{ddate},{"exit"}')

            elif (count%2 == 0):
                f.writelines(f'\n{name},{dtString},{ddate},{"entry"}')


start = time.time()
tx = 0
period = 50
face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
flag = 0
id = 0
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cas.detectMultiScale(gray, 1.3, 7)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, conf = recognizer.predict(roi_gray)


        if (conf < 70):
            stmt = 'SELECT * from student_details'
            cursor.execute(stmt)

            for row in cursor:
                if row[0] == id:
                    print("Id found\nWelcome " + row[1] + "\n")
                    tx = 1
                    break
            if tx == 0:
                print("Target not recognised")

        cv2.putText(img, str(id) + " " + str(conf), (x, y - 10), font, 0.55, (120, 255, 120), 1)

    cv2.imshow('frame', img)

    if flag == 10:

        break
    if time.time() > start + period:

        break
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

if tx==1:
    markAttendace(row[1])

cap.release()
cv2.destroyAllWindows()

