# Import required packages
import cv2
import pytesseract
import time

import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import time

def TTS(text1):
    print(text1)
    myobj = gTTS(text=text1, lang='en-us', tld='com', slow=False)
    myobj.save("voice.mp3")
    print('\n------------Playing--------------\n')
    song = MP3("voice.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load('voice.mp3')
    pygame.mixer.music.play()
    time.sleep(song.info.length)
    pygame.quit()

# import time
# import RPi.GPIO as GPIO
# 
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# 
# sw = 4
# GPIO.setup(sw, GPIO.IN)

while(True):
    cap = cv2.VideoCapture(0)
    while(True):
        ret, img = cap.read()
        if not ret:
            break
        
        cv2.imshow('result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('frame.png', img)
            cap.release()
            cv2.destroyAllWindows()
            break
#         
#         if GPIO.input(sw) == False:
#             cv2.imwrite('frame.png', img)
#             cap.release()
#             cv2.destroyAllWindows()
#             break

    img = cv2.imread('frame.png')
    img = cv2.resize(img, (960, 480))
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()
            
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    text1=''

    for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Apply OCR on the cropped image
            text1 += ''+pytesseract.image_to_string(cropped)

    try:
        TTS(text1)
    except:
        continue
