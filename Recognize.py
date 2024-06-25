import datetime
import os
import time
import cv2
import pandas as pd
from gtts import gTTS
import time
from pygame import mixer   
import os
from datetime import datetime
import pygame                  
import time                              #Import time library
import urllib3
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import serial



Intrudermsg="Intruder Detected"
Facemsg = "Autorized person Detected"

path="./img.jpg"

facethreshold=67

  
def sendmail():
    fromaddr = "18gowda2002@gmail.com"     #https://www.google.com/settings/security/lesssecureapps
    toaddr = "Venuhkhsn@gmail.com"
       
# instance of MIMEMultipart 
    msg = MIMEMultipart() 
# storing the senders email address   
    msg['From'] = fromaddr 
  
# storing the receivers email address  
    msg['To'] = toaddr 
  
# storing the subject  
    msg['Subject'] = "Alert!!..Intruder detected!!"
    
    # string to store the body of the mail 
    body = "Alert!!..Intruder detected!!"
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    
    # open the file to be sent  
    
    attachment = open(path, "rb") 
    
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(p) 
         
    # attach the instance 'p' to instance 'msg'
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % path)
    msg.attach(p) 
    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587)
    print("smtp",s)
        
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(fromaddr,"utnpmtpyhvjjllrc") 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string()
    print("text",text)
    
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
    s.quit()

def CallAudio(TextPhrase):
    # Language in which you want to convert
    language = 'en'  
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=TextPhrase, lang=language, slow=False)      
    # Saving the converted audio in a mp3 file named 
    now = datetime.now() 
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d%m%Y%H%M%S")
    MusicfileName = str("Welcome" + dt_string + ".mp3")
    #print(MusicfileName)
    myobj.save(MusicfileName)        
    PlayAudio(MusicfileName)
    print(TextPhrase)
    #print(MusicfileName)
    os.remove(MusicfileName)
        
def PlayAudio(FileName):
    # Starting the mixer
    mixer.init()      
    # Loading the song
    mixer.music.load(FileName)  
    print(FileName)    
    # Setting the volumee
    mixer.music.set_volume(0.7)      
    # Start playing the song
    mixer.music.play()  
    while pygame.mixer.music.get_busy() == True:
        continue
    # time.sleep(3)
    mixer.music.stop()
    mixer.quit()
    #pygame.event.wait()
    #infinite loop
    # while True:          
    #     print("Press 'p' to pause, 'r' to resume")
    #     print("Press 'e' to exit the program")
    #     query = input("  ")          
    #     if query == 'p':      
    #         # Pausing the music
    #         mixer.music.pause()     
    #     elif query == 'r':      
    #         # Resuming the musice
    #         mixer.music.unpause()
        # elif query == 'e':      
        #     # Stop the mixer
        #     mixer.music.stop()
        #     break
#-------------------------
def recognize_attendence():
    CallAudio("Started  Intruder detected system")
    print("Started  security IOT system")
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("./TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    CallAudio("Camera Intializing please wait")
    while True:
        _,im = cam.read()        
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 100 and conf>0:
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa
            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            tt = str(tt)[2:-2]
            if(100-conf) > facethreshold: #67
                tt = tt #+ " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
                CallAudio(Facemsg + tt)
                print(tt)
                print("Autorized person Detected")
                
            else:
                CallAudio(Intrudermsg)
                print(Intrudermsg)
                cv2.imwrite(path,im)
                sendmail()
                PlayAudio('alarm.mp3')
                time.sleep(10)
                
                
            #else:
                #cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

#             if (100-conf) > 67:
#                 cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
#             elif (100-conf) > 50:
#                 cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
#             else:
#                 cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

            #cv2.imshow('Attendance', im)

        #attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Face Detected', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    
    cam.release()
    cv2.destroyAllWindows()


