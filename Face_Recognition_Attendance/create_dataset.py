import cv2
import os
import numpy as np
from PIL import Image
from datetime import datetime
from datetime import date
import pypyodbc as odbc

Driver_name='SQL SERVER'
Server_name='LAPTOP-367JGRN0\ASWIN'
Database_name='Face_Recog'
cnxn = odbc.connect('DRIVER='+Driver_name+ ';'
                    'SERVER='+Server_name+';'
                   ' DATABASE=' + Database_name+' ;'
                   ' Trusted_Connection=yes;'
                    )

cursor=cnxn.cursor()


def create_ds(face_id):
    # Start capturing video
    vid_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize sample face image
    count = 0

    # Start loop
    while (True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes and list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x, y, w, h) in faces:
            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', image_frame)

        # If image taken reach 50, stop taking video
        if count >= 50:
            print("Successfully Captured")
            break
    # Stop video
    vid_cam.release()
    # Close all started windows
    cv2.destroyAllWindows()


print("Do you want to register a new user or update a existing user, \npress 1 for new user 2 for updating existing user")
x=int(input())
if(x==1):
    id=int(input('\nEnter id :'))
    name=input('\nEnter name :')
    date=date.today()
    insert_statement='''
        INSERT INTO student_details(Roll_No,Name,Date_Registered)
        VALUES(?,?,?)
    
    '''
    r = [id, name, date]
    try:
        cursor.execute(insert_statement, r)

    except Exception as e:
        cursor.rollback()
        print(e.value)
        print("\n Procedure failed")
    else:
        print("Records inserted successfully\n")
        cursor.commit()
        print("Please look into the camera\n")
        create_ds(id)

elif x==2:
    id=int(input('Enter your ID: '))
    stmt='SELECT * from student_details'
    cursor.execute(stmt)
    for row in cursor:
        if row[0]==id:
            print("Id found\nWelcome "+row[1]+"\nPlease look into the camera\n")
            create_ds(id)
            break;




else:
    print("Enter the correct number")


'''''''''
# Creating a dataset


face_id = input('enter your id ')
# Start capturing video
vid_cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Detect object in video stream using Haarcascade Frontal Face
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize sample face image
count = 0



# Start loop
while (True):

    # Capture video frame
    _, image_frame = vid_cam.read()

    # Convert to grayscale
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes and list of faces rectangles
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
    for (x, y, w, h) in faces:
        # Crop the image frame into rectangle
        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Increment sample face image
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        # Display the video frame, with bounded rectangle on the person's face
        cv2.imshow('frame', image_frame)



    # If image taken reach 50, stop taking video
    if count >= 50:
        print("Successfully Captured")
        break
# Stop video
vid_cam.release()
# Close all started windows
cv2.destroyAllWindows()

'''''
#######################################################################################





