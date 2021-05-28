import face_recognition
import cv2
import speech_test
import sqlite3 as sql
import recognize
import pyAurdi
import telebot


while True:
    help_text = """
Welcome to your DoorBot. I automatically decide who goes into your house for you. 
With your permission of course :)

Let me introduce you to the commands:

/help: To know more about Me ! 
/show: Send the most recent Picture of the Guest in the Database
/show_all: Send all the Pictures of the Guest in the Database
/open_door: Open the Door
/close_door: Close the Door 
    """

    CHAT_ID = '1069446040'
    API_KEY = '1817918162:AAFKEg0S50nZ8J6HlmGn3r1OrNeAWjaWZmg'
    bot = telebot.TeleBot(API_KEY)
    def kothamalli(str):
        bot.send_message(CHAT_ID, str)

    # Arduino open door serial command function
    @bot.message_handler(commands=['open_door'])
    def arduino_open_door(message):
        bot.send_message(message.chat.id, 'Door Has been Opened')
        print("Opening Door")
        pyAurdi.open_door()

    # Arduino close door serial command function
    @bot.message_handler(commands=['close_door'])
    def arduino_close_door(message):
        bot.send_message(message.chat.id, 'Door Has been Closed')
        print("Door Closed")
        pyAurdi.close_door()

    @bot.message_handler(commands=['help'])
    def greet(message):
        bot.reply_to(message, help_text)

    @bot.message_handler(commands=['show'])
    def greet(message):
        photo = open('./DataBase/test_pic_4.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

    @bot.message_handler(commands=['show_all'])
    def greet(message):
        photo0 = open('./DataBase/test_pic_0.jpg', 'rb')
        bot.send_photo(message.chat.id, photo0)  
        photo1 = open('./DataBase/test_pic_1.jpg', 'rb')
        bot.send_photo(message.chat.id, photo1)  
        photo2 = open('./DataBase/test_pic_2.jpg', 'rb')
        bot.send_photo(message.chat.id, photo2)
        photo3 = open('./DataBase/test_pic_3.jpg', 'rb')
        bot.send_photo(message.chat.id, photo3)
        photo4 = open('./DataBase/test_pic_4.jpg', 'rb')
        bot.send_photo(message.chat.id, photo4)
    bot.polling()

    #gesture detection
    gesture_result = recognize.main()

    #speech_detection
    speech_result = speech_test.voice()

    if(speech_result and gesture_result ):
        # converting assets to encoding
        # Load a sample picture and learn how to recognize it.
        sandhya_image = face_recognition.load_image_file("./Assets/sandhya.jpg")
        sandhya_face_encoding = face_recognition.face_encodings(sandhya_image)[0]

        makesh_image = face_recognition.load_image_file("./Assets/makesh.jpg")
        makesh_face_encoding = face_recognition.face_encodings(makesh_image)[0]

        harshith_image = face_recognition.load_image_file("./Assets/harshith.jpg")
        harshith_face_encoding = face_recognition.face_encodings(harshith_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            sandhya_face_encoding,
            harshith_face_encoding,
            makesh_face_encoding
        ]

        # A dictionary of Known Faces and who among them has the permission to allow unknown people inside.
        # The boolean value declares the permissio
        known_face_dict = {
            "Sandhya":True,
            "Harshith":False,
            "Makesh":True
        }


        # Making a list of the keys from the dictionary
        known_face_names = [name for name in known_face_dict.keys()]
        face_names = []            

        # Get a reference to webcam #0
        video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        # Taking 5 pics together for redundancy, incase 1 picture does not come proeprly
        for pic in range(5):
            # Grab a single frame of video
            ret, frame = video_capture.read()
            cv2.imwrite("./DataBase/test_pic_" + str(pic) + ".jpg", frame)

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
            
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imwrite("./DataBase/test_pic_" + str(pic) + ".jpg", frame)

        # Printing the recognized names just for reference
        print(face_names)
                
        boolean_list = []
        # finding out if the detected face is in the list of allowed members or not and replacing that plce with Boolean values
        for name in face_names:
            if name in known_face_names:
                boolean_list.append(True)
            else:
                boolean_list.append(False)

        # Create a list with boolean values mentioning if the person is allowed to enter with an unknown person or not
        dict_bool_list = [known_face_dict.get(name, False) for name in face_names]

        # Create a variable "boolean" with value True if Known person with access rights is at the door, or else False
        if any(dict_bool_list):
            boolean = any(boolean_list)
        else:
            boolean = all(boolean_list)

        # If the list is empty (no face detected) make 'boolean' as False 
        if len(face_names) < 1:
            print("Camera Blocked / or no face detected")
            boolean = False

        # Depnending on the value of "boolean" open the door or not
        if boolean:
            print("Door Open")
            kothamalli('The following guests have been allowed inside: ' + ', '.join(set(face_names)))            
            pyAurdi.open_door()
        else:
            print("Closed")
            if len(face_names) < 1:
                kothamalli('Someone is at the door but face has not been detected. Please check telegram')
                pyAurdi.close_door()
            else:
                kothamalli('Unknown person wants to enter. Please Enquire telegram for further details')
                pyAurdi.close_door()

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()  
