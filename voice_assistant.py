import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import re
from def_weather import *
from launch_app import *
import keyboard
import os
from os.path import exists
from jokeapi import Jokes
import asyncio
import tkinter as tk

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[3].id)

r = sr.Recognizer()


def speak(data):
    engine.say(data)
    engine.runAndWait()
    engine.stop()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = ("Jarvis")
    speak("I am your Assistant")
    speak(assname)

def todo_remind():
    with sr.Microphone() as source:
        speak('do u want me to remind ur todo list')
        while True:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                answer = r.recognize_google(audio)
                if 'yes' in answer.lower():
                    with open(f"{os.path.expanduser('~')}/Desktop/todo_list.txt") as file:
                        for line in file:
                            speak(line.rstrip())
                    break

                elif 'no' in answer.lower():
                    break

                else:
                    print('Please tell yes or no')
            except Exception as e:
                print('Please tell me again.')

def username():
    speak("Welcome Mister")
    speak(os.getlogin())

    if exists(f"{os.path.expanduser('~')}/Desktop/todo_list.txt"):
        todo_remind()

    speak("How can i Help you, Sir")

def popupmsg(msg, title):
    """Function for creating tkinter window that displays all commands"""

    popup = tk.Tk()
    popup.title(title)
    key_list = list(msg.keys())
    val_list = list(msg.values())
    for i in range (len(msg)):
        label = tk.Label(text=key_list[i]+': '+val_list[i])
        label.pack(side="top", fill="x", pady=5)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def takecommand():

    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            voice_data = r.recognize_google(audio, language="en")
            if 'Jarvis' in voice_data:
                speak("Yes sir...")
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                audio = r.record(source, duration=3)
                voice_data = r.recognize_google(audio, language="en").lower()

                return voice_data

        except sr.UnknownValueError:
            print("Repeat pls")

        except sr.RequestError:
            print("Repeat pls")

    return None

if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any command before execution of this python file
    clear()
    wishMe()
    username()

    while True:
        voice_data = takecommand()
        if voice_data != None:

            if re.search('what is|tell me about',voice_data):
                speak('Searching the internet...')
                query = voice_data.replace("what is", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                speak(results)

            if 'glory to ukraine' in voice_data:
                speak('Слава Україні')

            if 'what is your name' in voice_data:
                speak('My name is lefri')

            elif "date" in voice_data:
                date = datetime.datetime.now().strftime("%b %d %Y")
                speak(date)

            elif 'time' in voice_data:
                speak(datetime.datetime.now().strftime("%H:%M"))

            elif 'search' in voice_data:
                speak('What do you want to know?')
                search = takecommand()
                url = 'https://google.com/search?q=' + search
                webbrowser.get().open(url)

            elif 'open' in voice_data:
                voice_data = voice_data.replace('open ','')
                if 'youtube' in voice_data:

                    if 'music' in voice_data:
                        webbrowser.get().open('https://music.youtube.com/')

                    else:
                        webbrowser.get().open('https://youtube.com')

                elif 'google' in voice_data:
                    webbrowser.get().open('https://google.com')

                elif re.search('stack overflow|stackoverflow',voice_data):
                    webbrowser.get().open('https://stackoverflow.com/')

                elif 'tiktok' in voice_data:
                    webbrowser.get().open('https://www.tiktok.com')

                else:
                    try:
                        os.startfile(voice_data)

                    except FileNotFoundError:
                        app = program_open(voice_data)

                        if app == None:
                            speak('I cant find that program')

                        else:
                            os.startfile(app)

            elif re.match('close program|close app|close window', voice_data):
                keyboard.press('alt')
                keyboard.press('f4')
                keyboard.release('f4')
                keyboard.release('alt')

            elif 'sleep mode' in voice_data:
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

            elif 'turn off computer' in voice_data:
                os.system('shutdown -s -t 0')

            elif re.match('exit|stop', voice_data):
                speak('Bye, I was happy to help u')
                exit()

            elif 'joke' in voice_data:
                async def tell_joke():
                    j = await Jokes()  # Initialise the class
                    joke = await j.get_joke()  # Retrieve a random joke
                    if joke["type"] == "single":  # Print the joke
                        speak(joke["joke"])
                    else:
                        speak(joke["setup"])
                        speak(joke["delivery"])


                asyncio.run(tell_joke())

            elif 'what can you do' == voice_data:
                li_commands = {
                    "time": "Example: 'what time it is?'",
                    "date": "Example: 'what date it is?'",
                    "launch applications": "Example: 'open chrome'(can only launch app if it is in )",
                    "close app": "Example: 'close app/program/window'",
                    "tell me": "Example: 'tell me about India'",
                    "weather": "Example: 'what weather/temperature in Mumbai?'",
                    "news": "Example: 'news for today' ",
                    "opening sites": "Example: 'open google'(can open: tiktok, youtube, youtube music, stackoverflow)",
                    "whats is ...?": "Example: 'what is AI?'",
                    "add a task": "Creating to-do list and adding tasks to it. Example: 'add a task'",
                    "clear to-do list": "Clearing to-do list. Example: 'clear to do list'"
                }
                ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
                I can open websites for you, launch application and more. See the list of commands-"""
                speak(ans)
                popupmsg(li_commands, 'Commands')

            elif 'add a task' in voice_data:
                speak('What u want to add')
                task = takecommand()
                get_user = os.path.expanduser('~')
                with open(f'{get_user}/Desktop/todo_list.txt', 'a') as file:
                    file.write(f'{task}\n')
                    speak('Added succesfully')

            elif 'clear to-do list' in voice_data:
                speak('ur todo list now empty')
                open(f"{os.path.expanduser('~')}/Desktop/todo_list.txt", 'w').close()

            elif 'weather' in voice_data:
                speak('Name the city pls')
                city = takecommand()
                lc, wth, t = weather(city)
                speak(lc)
                speak(wth)
                speak(t)

            elif "temperature" in voice_data:
                speak('Name the city pls')
                city = takecommand()
                lc, wth, t = weather(city)
                speak(t)

            else:
                speak('I don`t have such command')
