import telebot
import pyAurdi

help_text = """
Welcome to your DoorBot. I automatically decide who goes into your house for you, with your permission of course :)

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