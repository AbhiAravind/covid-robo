import cv2,os
import numpy as np
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages');
import playsound
from playsound import playsound
from gtts import gTTS
import mysql.connector
from PIL import Image
from mysql.connector import Error
import PIL.Image
import serial
ser = serial.Serial ('/dev/ttyACM0')    #Open named port 
ser.baudrate = 9600

name_server = ''
Id = 0
Id_server=0
sampleNum=0
counter =0
phone_server=0
play_count =0
counter_frame=0
language = 'en'
previous_id=0
counter_image=0
Rover_movement_ID =1;
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces=faceCascade.detectMultiScale(imageNp)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids


def digital_to_binary(image_name):
        # Convert digital data to binary format
        with open(image_name, 'rb') as file:
            binaryData = file.read()
        return binaryData
playsound('/home/pi/Desktop/backup/New/audio/welcome.mp3')
playsound('/home/pi/Desktop/backup/New/audio/prihealth.mp3')
playsound('/home/pi/Desktop/backup/New/audio/intro.mp3')
db_connection = mysql.connector.connect(host='192.168.29.60',
                                         database='user_info',
                                         user='raspberrypi.domain.name',
                                         password='',
                                        )
db = db_connection
my_database = db_connection.cursor()
my_database1 = db_connection.cursor()
print(db)
ser.flush()

while True:
    ser.write(b'D')
    Serial_Db = ser.read(1)
    print(Serial_Db)
    if(Serial_Db ==b'D'):
        break
playsound('/home/pi/Desktop/backup/New/audio/dbconnection.mp3')
while True:
    ser.write(b'P')
    Serial_Pi = ser.read(1)
    print(Serial_Pi)
    if(Serial_Pi ==b'P'):
        break
playsound('/home/pi/Desktop/backup/New/audio/rover.mp3')
sql_statement = "SELECT id FROM info ORDER BY id DESC LIMIT 1;"
my_database.execute(sql_statement)
output = my_database.fetchall()
for loop_x in output:
  Id_server=int(loop_x[0])
 
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
print('Pi_Ready')
#font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
ser.flush()
ser.write(b'R')
playsound('/home/pi/Desktop/backup/New/audio/finalready.mp3')
while True:
    Rover_movement = ser.read(5)
    Rover_Rover_movement_ref = b'UStop'
    Rover_movement_ID=1
    if(Rover_movement == b'Front'):
        playsound('/home/pi/Desktop/backup/New/audio/front.mp3')
    if(Rover_movement == b'Back '):
        playsound('/home/pi/Desktop/backup/New/audio/back.mp3')
    if(Rover_movement == b'Left '):
        playsound('/home/pi/Desktop/backup/New/audio/left.mp3')
    if(Rover_movement == b'Right'):
        playsound('/home/pi/Desktop/backup/New/audio/right.mp3')

    if(Rover_movement == Rover_Rover_movement_ref):
        print(Rover_movement)
        Rover_movement=''
        sql_statement = "SELECT id FROM info ORDER BY id DESC LIMIT 1;"
        my_database.execute(sql_statement)
        output = my_database.fetchall()
        for loop_x in output:
          Id_server=int(loop_x[0])
        playsound('/home/pi/Desktop/backup/New/audio/camread.mp3')
        playsound('/home/pi/Desktop/backup/New/audio/move_lock.mp3')
        cam = cv2.VideoCapture(0)
        while True:
            ret, im =cam.read()   
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            print("no frame")
            counter_frame = counter_frame + 1
            if(counter_frame == 50):
                ser.write(b'r')
                counter_frame=0
                playsound('/home/pi/Desktop/backup/New/audio/no_face.mp3')
                break
            for(x,y,w,h) in faces:
                print("image")
                counter_frame = 0
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                if(conf<50):
                    print(conf)
                    counter =0
                    counter_image = counter_image+1
                    if(counter_image>4):
                        ser.write(b'*')
                        playsound('/home/pi/Desktop/backup/New/audio/facerec.mp3')
                        previous_id=0
                        counter_image=0
                        print("Id value = %d"%Id)
                        sql_statement_name ="SELECT name, phone FROM info WHERE id=%d;"%Id
                        print(sql_statement_name)
                        my_database.execute(sql_statement_name)
                        output2 = my_database.fetchall()
                        for loop_y in output2:    
                            name_server=loop_y[0]
                            phone_server=loop_y[1]
                        print(output2)
                        print(name_server)
                        print(phone_server)
                        print(Id)
                        trans_name = (str(name_server)+'#').encode('UTF-8')
                        trans_phone = (str(phone_server)+'#').encode('UTF-8')
                        ser.write(trans_name)
                        ser.write(trans_phone)
                        playsound('/home/pi/Desktop/backup/New/audio/hello.mp3')
                        mytext = name_server
                        myobj = gTTS(text=mytext, lang=language)
                        myobj.save("dynamic.mp3")
                        playsound('dynamic.mp3')
                        playsound('/home/pi/Desktop/backup/New/audio/phone.mp3')
                        mytext1 = str(phone_server)
                        mytext2 = " ".join(mytext1)
                        print(mytext2)
                        myobj = gTTS(text=mytext2, lang=language)
                        myobj.save("dynamic_phone.mp3")
                        playsound('dynamic_phone.mp3')
                        ser.flush()
                        print(trans_name)
                        playsound('/home/pi/Desktop/backup/New/audio/sensor1.mp3')
                        while True:
                            ser.write(b'H')
                            if(ser.inWaiting()):
                                Temp = ser.read(10)
                                print(Temp)
                                if(Temp == b'Terminated'):
                                    break
                                else:
                                    data_temp_heart = Temp
                        print(data_temp_heart)
                        playsound('/home/pi/Desktop/backup/New/audio/hands.mp3')
                        temp_str = chr(data_temp_heart[4])+chr(data_temp_heart[5])+chr(data_temp_heart[6])
                        temp = int(temp_str)
                        temp1=str(temp)
                        temp2 = " ".join(temp1)
                        myobj = gTTS(text=temp2, lang=language)
                        myobj.save("dynamic_temp.mp3")
                        playsound('/home/pi/Desktop/backup/New/audio/temp_is.mp3')
                        playsound('dynamic_temp.mp3')
                        Hear_beat_str = chr(data_temp_heart[0])+chr(data_temp_heart[1])+chr(data_temp_heart[2])
                        Hear_beat =int(Hear_beat_str)
                        heart_beat1=str(Hear_beat)
                        heart_beat2 = " ".join(heart_beat1)
                        myobj = gTTS(text=heart_beat2, lang=language)
                        myobj.save("dynamic_heart.mp3")
                        playsound('/home/pi/Desktop/backup/New/audio/heart_beat.mp3')
                        playsound('dynamic_heart.mp3')
                        sql_update = """UPDATE info SET temp= %d,pulse= %d  WHERE id = %d """%(temp,Hear_beat,Id)
                        my_database.execute(sql_update)
                        db_connection.commit()
                        ser.write(b'Db_update')
                        ser.flush()
                        Rover_movement_ID =0
                        if(temp>100):
                            playsound('/home/pi/Desktop/backup/New/audio/take_care.mp3')
                        else:
                            playsound('/home/pi/Desktop/backup/New/audio/thanks.mp3')
                else:
                    counter = counter +1
                    print("Counter %d"%counter)
                    if(counter == 30):
                            previous_id=0
                            counter_image=0
                            name_server="Unknown"
                            counter=0
                #cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
                cv2.putText(im, str(name_server), (x,y+h),font,1,(255, 255,255),2, cv2.LINE_AA)
            cv2.imshow('im',im)
            if(Rover_movement_ID == 0 ):
                ser.write(b'r')
                cam.release()
                cv2.destroyAllWindows()
                break
            if name_server == "Unknown":
                ser.write(b'*')
                playsound('/home/pi/Desktop/backup/New/audio/unknown.mp3')
                Id_num=Id_server+1
                playsound('/home/pi/Desktop/backup/New/audio/input_name.mp3')
                name_input = input("Enter your name")
                myobj = gTTS(text=name_input, lang=language)
                myobj.save("dynamic_name1.mp3")
                playsound('/home/pi/Desktop/backup/New/audio/name_is.mp3')
                playsound('dynamic_name1.mp3')
                playsound('/home/pi/Desktop/backup/New/audio/enter_phone.mp3')
                phone_input = input("Enter your phone")
                phone_input1=str(phone_input)
                phone_input2 = " ".join(phone_input1)
                myobj = gTTS(text=phone_input2, lang=language)
                myobj.save("dynamic_phone1.mp3")
                playsound('/home/pi/Desktop/backup/New/audio/phone_is.mp3')
                playsound('dynamic_phone1.mp3')
                trans_name = (str(name_input)+'#').encode('UTF-8')
                trans_phone = (str(phone_input)+'#').encode('UTF-8')
                ser.write(trans_name)
                ser.write(trans_phone)
                name_server =''
                sampleNum=0
                playsound('/home/pi/Desktop/backup/New/audio/keep_eye.mp3')
                while(True):
                    
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                    for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        #incrementing sample number 
                        sampleNum=sampleNum+1
                        #saving the captured face in the dataset folder
                        cv2.imwrite("dataSet/User."+str(Id_num) +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                        cv2.imshow('frame',img)
                        
                    if sampleNum>30:
                        ser.write(b'NewImage')
                        print("New Image Training finished")
                        faces,Ids = getImagesAndLabels('dataSet')
                        recognizer.train(faces, np.array(Ids))
                        recognizer.write('trainner/trainner.yml')
                        ser.flush()
                        playsound('/home/pi/Desktop/backup/New/audio/recorded.mp3')
                        playsound('/home/pi/Desktop/backup/New/audio/sensor1.mp3')
                        while True:
                            ser.write(b'H')
                            if(ser.inWaiting()):
                                Temp = ser.read(10)
                                if(Temp == b'Terminated'):
                                    break
                                else:
                                    data_temp_heart = Temp
                        print(data_temp_heart)
                        playsound('/home/pi/Desktop/backup/New/audio/hands.mp3')
                        temp_str = chr(data_temp_heart[4])+chr(data_temp_heart[5])+chr(data_temp_heart[6])
                        temp = int(temp_str)
                        print(temp)
                        temp1=str(temp)
                        temp2 = " ".join(temp1)
                        myobj = gTTS(text=temp2, lang=language)
                        myobj.save("dynamic_temp.mp3")
                        playsound('/home/pi/Desktop/backup/New/audio/temp_is.mp3')
                        playsound('dynamic_temp.mp3')
                        Hear_beat_str = chr(data_temp_heart[0])+chr(data_temp_heart[1])+chr(data_temp_heart[2])
                        Hear_beat =int(Hear_beat_str)
                        heart_beat1=str(Hear_beat)
                        heart_beat2 = " ".join(heart_beat1)
                        myobj = gTTS(text=heart_beat2, lang=language)
                        myobj.save("dynamic_heart.mp3")
                        playsound('/home/pi/Desktop/backup/New/audio/heart_beat.mp3')
                        playsound('dynamic_heart.mp3')
                        image_pi = "dataSet/User."+str(Id_num) +'.'+ str(sampleNum) + ".jpg"
                        Picture_pi = digital_to_binary(image_pi)
                        print(phone_input)
                        my_database1.execute("INSERT INTO info (name, phone, temp, pulse, photo) VALUES (%s, %s, %s, %s, %s)", (name_input, phone_input, temp, Hear_beat, Picture_pi))
                        db_connection.commit()
                        ser.write(b'Db_Insert')
                        Rover_movement_ID =0;
                        ser.flush()
                        if(temp>100):
                            playsound('/home/pi/Desktop/backup/New/audio/take_care.mp3')
                        else:
                            playsound('/home/pi/Desktop/backup/New/audio/thanks.mp3')
                        break;
                   
            if cv2.waitKey(10) & 0xFF==ord('q'):
                break
        cam.release()  
    else:
        print(Rover_movement)

cv2.destroyAllWindows()       
ser.close()

