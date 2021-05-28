import speech_recognition as sr
r = sr.Recognizer()
# def recogVoice(audio):
#     try:
#         return r.recognize_google(audio)
#     except:
#         return ''
def voice():
    while True:
        with sr.Microphone() as source :
            print(" Please tell your code ")
            r.adjust_for_ambient_noise(source, duration=2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            code = format(text)
            print(code)
            if(code=="open door"):
                return True
            elif (code=="close door"):
                print("Door Has Been Closed")
                return False
            else:
                print("Could not Recognise your Voice.")
                return False