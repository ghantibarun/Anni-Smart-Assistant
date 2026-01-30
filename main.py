from time import strftime
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import datetime
import random
from openai import OpenAI
#from openaitest import client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(base_url="https://api.groq.com/openai/v1")

chat_history = [
    {"role": "system", "content": "You are Anni, a helpful AI assistant."}
]

def chat(query):
    global chat_history
    client = OpenAI(base_url="https://api.groq.com/openai/v1")

    # Nilu speaks
    print(f"Nilu: {query}")

    chat_history.append({
        "role": "user",
        "content": query
    })

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=chat_history,
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        # Anni speaks
        print(f"Anni: {answer}")
        say(answer[:50])

        chat_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as e:
        print("Chat Error:", e)
        say("Sorry sir I faced an error.")
        return ""

def ai(prompt):

    text = f"OpenAi response for prompt: {prompt} \n *********************\n\n"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        print(response.choices[0].message.content)
        text += response.choices[0].message.content
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        #with open(f"Openai/prompt_{random.randint(1,999999)}.txt","w",encoding="utf-8") as f:
        with open(f"Openai/{''.join(prompt.split('AI')[1:])}.txt","w",encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print("AI Error:", e)
        say("Sorry, I faced an error while using AI")

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query
    except Exception as e:
        return "Some error occurred. Sorry from Anni"


if __name__ == '__main__':
    print('PyCharm')
    say("Hello I am Anni")

    while True:
        print("Listening...")
        query = takeCommand()

        #todo: Add more sites
        sites = [["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.com"],
                 ["google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open_new_tab(site[1])

        #todo: Add a feature to play a specific song
        if "open music" in query:
            musicpath = r"C:\My\Main Rang Sharbaton Ka _ Arijit Singh _ Phata Poster Nikhla Hero _ 2013(MP3_160K).mp3"
            os.startfile(musicpath)
        if "the time" in query:
            strftime = datetime.datetime.now().strftime("%H:%M %S")
            say(f"Sir the time is {strftime}")

        apps = {
            "calculator": "calculator:",
            "settings": "ms-settings:",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        }
        for app in apps:
            if f"open {app}" in query.lower():
                say(f"Opening {app} sir...")
                try:
                    os.startfile(apps[app])
                except:
                    say("Sorry, I cannot open this app")

        if "Using AI".lower() in query.lower():
            ai(prompt=query)

        elif any(word in query.lower() for word in ("exit", "quit", "stop")):
            say("Thank you and Good bye")
            break
        elif "reset chat".lower() in query.lower():
            chatstr = ""

        else:
            print("Chating...")
            chat(query)
