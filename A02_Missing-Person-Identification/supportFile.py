import face_recognition
import cv2
import time
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1723728383<0 else 0
import os
import pywhatkit
import pyautogui 
import keyboard as k 
import numpy



i=0
f_image = []
known_face_names = []
known_face_encodings = []

face_locations = []
face_encodings = []
face_names = []

# for filename in os.listdir("dataset"):
# 	known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file("dataset/"+filename))[0])
# 	known_face_names.append(filename.split('.')[0])
# 	i = i + 1
for filename in os.listdir("dataset"):
    try:
        encoding = face_recognition.face_encodings(face_recognition.load_image_file("dataset/" + filename))
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(filename.split('.')[0])
            i += 1
    except Exception as e:
        print(f"Error processing image {filename}: {e}")


process_this_frame = True

prename=''
def get_frame(video=0):
	global process_this_frame
	global prename

	video_capture = cv2.VideoCapture(0)
	# time.sleep(2.0)

	while True:
		ret, frame = video_capture.read()

	
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

		
		rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])

	
		if process_this_frame:
		
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			face_names = []
			for face_encoding in face_encodings:
				
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
				name = "Unknown"

			
				if True in matches:
					first_match_index = matches.index(True)
					name = known_face_names[first_match_index]

				face_names.append(name)

		process_this_frame = not process_this_frame


		
		for (top, right, bottom, left), name in zip(face_locations, face_names):
		
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

		
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

			print(name)
			if(name != 'Unknown'):
				cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, "Missing Person Detected: "+name, (20, 20), font, 1.0, (255, 255, 255), 1)
				cv2.imwrite('detected.jpg',frame)
				if(name!=prename):
					
					pywhatkit.sendwhatmsg_instantly("+918379975886",name+' found at Modern College Canteen')	
					#pywhatkit.sendwhats_image("+919518731289",'detected.jpg',name+' found at busstop')
					# pyautogui.click(1050,950)
					
					time.sleep(10)
					pyautogui.click(683, 384)
					k.press_and_release('enter')
					prename=name 

						
			
		imgencode=cv2.imencode('.jpg',frame)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	# video_capture.release()
	# cv2.destroyAllWindows()

# Main function
if __name__ == "__main__":
    for frame in get_frame():
        # Do something with the frame, e.g., display it
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
