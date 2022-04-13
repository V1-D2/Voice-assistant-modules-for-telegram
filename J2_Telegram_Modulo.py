import configparser
import telethon
import pyttsx3
import speech_recognition as sr
import pyautogui as pg

from telethon import TelegramClient
from telethon import sync
from telethon import events
from telethon import connection

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChannelParticipantsSearch

from datetime import date, datetime

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config["Telegram"]["api_id"]
api_hash = config["Telegram"]["api_hash"]
username = config["Telegram"]["username"]
my_id = config["Telegram"]["my_id"]


client = TelegramClient(username, api_id, api_hash)

baseOfUserId = {}
fin = open("User_Id.txt", "r")
for line in fin:
    ar = [ i for i in line.strip().split(" = ")]
    baseOfUserId[ar[0]] = ar[1]
    


@client.on(events.NewMessage(chats = ('DVueh')))
async def normal_hundler(event):
    if(event.message.to_dict()['from_id']['user_id'] != int(my_id)):
        speak(event.message.to_dict()['message'])
        await getAnswer('DVueh', event.message.to_dict())

@client.on(events.NewMessage(chats = ('the_best_tm')))
async def normal_hundler(event):
    if (event.message.to_dict()['from_id']['user_id'] != int(my_id)):
        speak(event.message.to_dict()['message'])
        await getAnswer('the_best_tm', event.message.to_dict())

@client.on(events.NewMessage(chats = ('Diaall')))
async def normal_hundler(event):
    if (event.message.to_dict()['from_id']['user_id'] != int(my_id)):
        speak(event.message.to_dict()['message'])
        await getAnswer('Diaall', event.message.to_dict())
@client.on(events.NewMessage(chats = ('TBCbas')))
async def normal_hundler(event):
    if (event.message.to_dict()['from_id']['user_id'] != int(my_id)):
        speak(event.message.to_dict()['message'])
        await getAnswer('TBCbas', event.message.to_dict())
@client.on(events.NewMessage(chats = ('ternopilskaODA')))
async def normal_hundler(event):
    print(event.message)
    message = event.message.to_dict()["message"].lower()
    if("повітряна тривога" in message):
        for i in range(3):
            speak(event.message.to_dict()['message'])
            speak("Все документы лежат на кушетке возле входной двери, или уже в гараже")
    elif("відбій" in message):
        for i in range(3):
            speak("Подождите ещё 3 минуты и можете выходить")
    elif("гуманітарна" in message or "допомога" in massage or "пенсі" in message):
        for i in range(3):
            speak("Есть важная информация о пенсиях или гуманитарной помощи")
            speak(message)
            speak("Я открою телеграм для уточнения")
        try:
            os.system(r'C:\"Users"\"Dell e7450"\"AppData"\"Roaming"\"Telegram Desktop"\Telegram.exe')
        except:
            speak("Попробую по другому")
            try: os.startfile(r'c:\"Users"\"Dell e7450"\"AppData"\"Roaming"\"Telegram Desktop"\Telegram.exe')
            except: speak("Напишите Вове, тут скорее всего ошибка или особенность системы")
        finally: pg.sleep(2)
        #open channel with notification
        pg.click(130,80)
        pg.sleep(3)
        pr.typewrite(f"@ternopilskaODA")
        pg.typewrite(['Enter'])
















#Functions
async def getAnswer(username, message):
    whatAndWho = [message["message"], message['peer_id']['user_id']]
    speak("Хотите ответить?")
    try:
        answer = listenTheAnswer()
        if ("да" in answer or "давай" in answer or "хочу" in answer):
            await client.send_message(username, listenTheAnswer())
        elif ("не" in answer or "нет" in answer or "нехочу" in answer):
            fin = open("Missed_Massages.txt", "a")
            userName = baseOfUserId[str(whatAndWho[1])]
            if isinstance(message["date"], datetime):
                time = str(int(message["date"].isoformat()[11::-11])+2)+str(message["date"].isoformat())[13:][:3]
            fin.write(whatAndWho[0]+", " + userName + ", " + time + "\n")
            fin.close()
            speak("Сохранено в непрочитанные)")
    except sr.UnknownValueError:
        speak("[log] Голос не распознан!, сохранено в непроверенные)")
        fin = open("Missed_Massages.txt", "a")
        userName = baseOfUserId[str(whatAndWho[1])]
        if isinstance(message["date"], datetime):
            time = str(int(message["date"].isoformat()[11::-11]) + 2) + str(message["date"].isoformat())[13:][:3]
        fin.write(whatAndWho[0] + ", " + userName + ", " + time + "\n")
        fin.close()
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

"""Speak and Listen Functions"""
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()

def listenTheAnswer():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as audio_file:
        r.adjust_for_ambient_noise(audio_file)
        print("Говорите")
        audio = r.listen(audio_file)
        return r.recognize_google(audio, language="ru-RU").lower()
"""End"""


#voice
speak_engine = pyttsx3.init("sapi5")
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

client.start()
client.run_until_disconnected()